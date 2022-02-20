using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace ConsoleApplication1
{
    // The class has member variables to match the BGP update message attributes.
    class bgp_updates
    {
        string TYPE; //The type of BGP message: update, open, keepalive, notificaiton
        string FROM; //The IP of the sender BGP peer
        string TO; //The IP of the reciever BGP peer
        string BGP_PACKET_TYPE; //The type of BGP message: update, open, keepalive, notificaiton
        string AS_PATH; //The AS-PATH attribute of BGP message
        string NEXT_HOP; //The Next-HOP attribute of BGP messege 
        string ORIGIN; //The ORIGIN attribute of BGP message: IGP, EGP, or Incomplete
        string COMMUNITY_ATTRIBUTTES; //The commuinity attribute of BGP update message   
        DateTime DATE; // The date when BGP message was send
        int SIZE; //The size of BGP message in Bytes.
        
        List <string> ANNOUNCED_NLRI= new List<string>(); //The NLRI prefixes that were announced inside a BGP message
        List<string> WITHDRAWN = new List<string>(); //The NLRI prefixes that were withdrawn inside the BGP message

        //Properties
        public int sIZE
        {
            get { return SIZE; }
            set { SIZE = value; }
        }

        public string cOMMUNITY_ATTRIBUTTES
        {
            get { return COMMUNITY_ATTRIBUTTES; }
            set { COMMUNITY_ATTRIBUTTES = value; }
        }

        public DateTime date
        {
            get { return DATE; }
            set { DATE = value; }
        }
    
        public string type
        {
            get { return TYPE; }
            set { TYPE = value; }
        }
        public string from
        {
            get { return FROM; }
            set { FROM = value; }
        }
        public string to
        {
            get { return TO; }
            set { TO = value; }
        }

        public string bgp_packet_type
        {
            get { return BGP_PACKET_TYPE; }
            set { BGP_PACKET_TYPE = value; }
        }

        public string as_path
        {
            get { return AS_PATH; }
            set { AS_PATH = value; }
        }

        public string Next_Hop
        {
            get { return NEXT_HOP; }
            set { NEXT_HOP = value; }
        }

        public List<string> Announced
        {
            get { return ANNOUNCED_NLRI; }
            set { ANNOUNCED_NLRI = value; }
        }

        public List<string> WITHDRAWn
        {
            get { return WITHDRAWN; }
            set { WITHDRAWN = value; }
        }

        public string origin
        {
            get { return ORIGIN; }
            set { ORIGIN = value; }
        }
    }
}
