import logging
from redzoo.database.simple import SimpleDB
from abc import ABC, abstractmethod
from threading import Thread
from typing import List
import enocean.utils
from enocean.communicators.serialcommunicator import SerialCommunicator
from enocean.protocol.constants import PACKET, RORG
import queue


logging.basicConfig(format='%(asctime)s %(name)-20s: %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')




class Device:

    def handle_packet(self, packet) -> bool:
        pass


class DeviceListener(ABC):

    @abstractmethod
    def on_updated(self, device: Device):
        pass


class WindowHandle(Device):

    @staticmethod
    def supports(eep_id: str) -> bool:
        return eep_id.upper() == 'F6:10:00'

    def __init__(self, name: str, eep_id: str, enocean_id: str, listener: DeviceListener):
        self.listener = listener
        self.name = name
        self.db = SimpleDB("processing_state_" + eep_id + "_" + enocean_id)
        self.sender = enocean_id.upper()
        self.sender_hex_string: List[int] = enocean.utils.from_hex_string(self.sender)
        self.eep_id = eep_id.upper()
        self.eep_id_hex_string: List[int] = enocean.utils.from_hex_string(self.eep_id)
        logging.info("window handle (eep_id: " + eep_id + ", enocean_id: " + enocean_id +")")

    @property
    def state(self) -> int:
        return self.db.get("state", 3)

    @property
    def state_text(self) -> str:
        if self.state == 1:
            return "TILTED"
        elif self.state == 2:
            return "OPEN"
        else:
            return "CLOSED"

    def handle_packet(self, packet) -> bool:
        is_handled = False
        try:
            if self.eep_id_hex_string[0] == 0xf6 and packet.packet_type == PACKET.RADIO_ERP1 and packet.rorg == RORG.RPS:
                packet.parse_eep(self.eep_id_hex_string[1], self.eep_id_hex_string[2])
                state = packet.parsed['WIN']['raw_value']  #  WIN: {'description': 'Window handle', 'unit': '', 'value': 'Moved from vertical to down', 'raw_value': 3}
                if self.sender == packet.sender_hex:
                    self.db.put("state", state)
                    logging.info(self.name + " state updated " + self.state_text)
                    self.listener.on_updated(self)
                    is_handled = True
        except Exception as e:
            logging.warning("error occurred by handling packet", e)
        return is_handled



class Enocean:

    def __init__(self, port: str, devices: List[Device]):
        self.running = True
        self.devices = devices
        self.communicator = SerialCommunicator(port=port)

    def stop(self):
        self.running= False

    def receive(self, background: bool = False):
        if background:
            Thread(target=self.__receive, daemon=True).start()
        else:
            self.__receive()

    def __receive(self):
        try:
            self.communicator.start()
            if self.communicator.base_id is None:
                logging.warning('init failed')
            else:
                logging.info('The Base ID of your module is %s.' % enocean.utils.to_hex_string(self.communicator.base_id))

            # endless loop receiving radio packets
            while self.communicator.is_alive() and self.running:
                try:
                    # Loop to empty the queue...
                    packet = self.communicator.receive.get(block=True, timeout=1)
                    for device in self.devices:
                        is_handled = device.handle_packet(packet)
                        if is_handled:
                            break
                except queue.Empty:
                    continue
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    logging.warning("error occurred by processing packet", e)
        finally:
            self.communicator.stop()


