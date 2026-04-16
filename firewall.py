from ryu.app import simple_switch_13
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3

class MyFirewall(simple_switch_13.SimpleSwitch13):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(MyFirewall, self).__init__(*args, **kwargs)
        # Target: h1 (using --mac flag in mininet)
        self.banned_host = '00:00:00:00:00:01'

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        # 1. INSTALL BLOCK RULE: TCP Port 80 for h1
        # eth_type=0x0800 (IPv4), ip_proto=6 (TCP)
        match_tcp = parser.OFPMatch(
            eth_src=self.banned_host,
            eth_type=0x0800,
            ip_proto=6,
            tcp_dst=80
        )
        
        # Priority 30 (Very High) - No actions [] means DROP
        self.add_flow(datapath, 30, match_tcp, [])
        print(f"!!! FIREWALL: TCP Port 80 blocked for {self.banned_host}")

        # 2. INSTALL ALLOW RULE: Everything else (like Pings)
        # This is the default "miss" entry
        match_else = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match_else, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)
