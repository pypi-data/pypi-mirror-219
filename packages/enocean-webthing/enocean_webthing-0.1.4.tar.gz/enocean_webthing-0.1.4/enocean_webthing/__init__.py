from string import Template
from enocean_webthing.app import App
from enocean_webthing.enocean_webthing import run_server

PACKAGENAME = 'enocean_webthing'
ENTRY_POINT = "enocean"
DESCRIPTION = "A web connected enocean gateway"


UNIT_TEMPLATE = Template('''
[Unit]
Description=$packagename
After=syslog.target

[Service]
Type=simple
ExecStart=$entrypoint --command listen --verbose $verbose --port $port --path $path --devices '$devices'  
SyslogIdentifier=$packagename
StandardOutput=syslog
StandardError=syslog
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
''')



class GatewayApp(App):


    def do_process_command(self, command:str, port: int, verbose: bool, args) -> bool:
        if command == 'listen':
            print("running " + self.packagename + " on port " + str(port))
            addresses = [address.strip() for address in args.devices.split(",")]
            run_server(port, self.description, args.path, addresses)
            return True
        elif args.command == 'register':
            print("register " + self.packagename + " on port " + str(port) + " and starting it")
            unit = UNIT_TEMPLATE.substitute(packagename=self.packagename,
                                            entrypoint=self.entrypoint,
                                            port=port,
                                            verbose=verbose,
                                            path=args.path,
                                            devices=args.devices)
            self.unit.register(port, unit)
            return True
        else:
            return False


def main():
    GatewayApp(PACKAGENAME, ENTRY_POINT, DESCRIPTION).handle_command()


if __name__ == '__main__':
    main()
