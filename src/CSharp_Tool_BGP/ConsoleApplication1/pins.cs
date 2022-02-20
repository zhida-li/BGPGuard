using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace ConsoleApplication1
{
    class pins
    {
        int Count; // The counter of BGP messaged in each 1 pin (match 1 minute period of time)
        int Count_as; //The counter of BGP messaged that has an AS-PATH attribute in it (Announcment messages only) to compuet the AvgAsPath member variable
        int Count_unique_as; //The counter of the BGP messaged that have an unique AS-PATH attribute in it (Announcment messages only) to compuet the AvgAsPath member variable
        DateTime Time; //The time of the pin during the day. It takes 1440 different values (the time of the minute during the day)
        int NumberOfannouncedPrefixes; // The total number of the announced prefixes for each 1 minute period of time 
        int NumberOfWithdrawnsPrefixes; // The total number of withdrawn prefixes for eacdh 1 minute period of time 
        int NumberOfAnnouncments; //The total number of BGP update messages that announce NLRIs
        int NumberOfWithdrawals; //The total number of BGP update messages that withdraw NLRIs
        int NumberOfUpdates; //The total number of BGP update messages that announce or withdraw NLRIs

        double AvgAsPath; //The average AS-PATH length of all the packets for each 1 minute period of time.
        double MaxAsPath; //The maximum AS-PATH length of all the packets for each 1 minute period of time
        double MaxUniqueAsPath; //The maximum AS-PATH length of all the packets for each 1 minute period of time that has a unique AS-PATH //It is the same as MaxAsPath
        double AvgUniqueAsPath; //The average AS-PATH length of all the packets for each 1 minute period of time that has a unique AS-PATH
        List<string> Unique_AS_Path = new List<string>(); //List of all unique AS-PATHs in 1 minute period of time. 

        //Data members for duplicates messages
        int DuplicateBGPAnnouncements;    //The number of Duplicate BGP announcment messages 
        List<bgp_updates> PinsBGPUpdates = new List<bgp_updates>();
        int DuplicateBGPWithdrawls;  //The number of Duplicate BGP withdrawal messages 
        int NADA; //The number of BGP messages that has new announcment but different attributes
        int ImplicitWithdrawals; // the number of BGP messages that were announced before and are announced again with differenet AS-PATH

        //Edit Distance
        int MaximumAsPathEditDistnace; //The maximum edit distance for the AS-PATH attribute
        int AverageAsPathEditDistnace; //The average edit distance for the AS-PATH attribute 
        int MinimumAsPathEditDistnace; //The minimum edit distance for the AS-PATH attribute 

        //Origin
        int NumberOfIGP; //The number of IGP BGP packets for each 1 minute period of time
        int NumberOfEGP; //The number of EGP BGP packets for each 1 minute period of time
        int NumberOfIncomplete; //The number of Incomplete BGP packets for each 1 minute period of time

        //OPEN +KEEP ALIVE+NOTIFICATION
        int NumberOfOPENMessages; // The number of OPEN messages for each 1 minute period of time
        int NumberOfKeepAliveMessages; //The number of Keepalive messages for each 1 minute period of time
        int NumberOfUPDATEMessages; //The number of UPDATE messages for each 1 minute period of time. It is also used as counter for number of messeges in each pin
        int NumberOfNOTIFICATIONMessages; //The number of Notification messages for each 1 minute period of time

        //PIN Average size
        int AvgSize; //The average packet size in bytes. 

        //Properties
        public int count
        {
            get { return Count; }
            set { Count = value; }
        }
        public int AVGSize
        {
            get { return AvgSize; }
            set { AvgSize = value; }
        }
        public int numberOfOPENMessages
        {
            get { return NumberOfOPENMessages; }
            set { NumberOfOPENMessages = value; }
        }
        public int numberOfKeepAliveMessages
        {
            get { return NumberOfKeepAliveMessages; }
            set { NumberOfKeepAliveMessages = value; }
        }
        public int numberOfUPDATEMessages
        {
            get { return NumberOfUPDATEMessages; }
            set { NumberOfUPDATEMessages = value; }
        }
        public int numberOfNOTIFICATIONMessages
        {
            get { return NumberOfNOTIFICATIONMessages; }
            set { NumberOfNOTIFICATIONMessages = value; }
        }
        public int numberOfIGP
        {
            get { return NumberOfIGP; }
            set { NumberOfIGP = value; }
        }
        public int numberOfEGP
        {
            get { return NumberOfEGP; }
            set { NumberOfEGP = value; }
        }
        public int numberOfIncomplete
        {
            get { return NumberOfIncomplete; }
            set { NumberOfIncomplete = value; }
        }

        public int minimumAsPathEditDistnace
        {
            get { return MinimumAsPathEditDistnace; }
            set { MinimumAsPathEditDistnace = value; }
        }
        public int averageAsPathEditDistnace
        {
            get { return AverageAsPathEditDistnace; }
            set { AverageAsPathEditDistnace = value; }
        }

        public int maximumAsPathEditDistnace
        {
            get { return MaximumAsPathEditDistnace; }
            set { MaximumAsPathEditDistnace = value; }
        }

        public int duplicateBGPWithdrawls
        {
            get { return DuplicateBGPWithdrawls; }
            set { DuplicateBGPWithdrawls = value; }
        }
        public int nADA
        {
            get { return NADA; }
            set { NADA = value; }
        }
        public int implicitWithdrawals
        {
            get { return ImplicitWithdrawals; }
            set { ImplicitWithdrawals = value; }
        }

        public List<bgp_updates> pinsBGPUpdates
        {
            get { return PinsBGPUpdates; }
            set { PinsBGPUpdates = value; }
        }

        public int duplicateBGPAnnouncements
        {
            get { return DuplicateBGPAnnouncements; }
            set { DuplicateBGPAnnouncements = value; }
        }
        public int count_as
        {
            get { return Count_as; }
            set { Count_as = value; }
        }
        public int count_unique_as
        {
            get { return Count_unique_as; }
            set { Count_unique_as = value; }
        }
        public DateTime time
        {
            get { return Time; }
            set { Time = value; }
        }
        public int NumberOfAnnouncedPrefixes
        {
            get { return NumberOfannouncedPrefixes; }
            set { NumberOfannouncedPrefixes = value; }
        }
        public int NumberOfwithdrawnsPrefixes
        {
            get { return NumberOfWithdrawnsPrefixes; }
            set { NumberOfWithdrawnsPrefixes = value; }
        }
        public int NumberofAnnouncments
        {
            get { return NumberOfAnnouncments; }
            set { NumberOfAnnouncments = value; }
        }
        public int NumberofWithdrawals
        {
            get { return NumberOfWithdrawals; }
            set { NumberOfWithdrawals = value; }
        }
        public int NumberofUpdates
        {
            get { return NumberOfUpdates; }
            set { NumberOfUpdates = value; }
        }
        public double AvgASPath
        {
            get { return AvgAsPath; }
            set { AvgAsPath = value; }
        }
        public double MaxASPath
        {
            get { return MaxAsPath; }
            set { MaxAsPath = value; }
        }
        public double maxUniqueASPath
        {
            get { return MaxUniqueAsPath; }
            set { MaxUniqueAsPath = value; }
        }
        public double AvgUniqueASPath
        {
            get { return AvgUniqueAsPath; }
            set { AvgUniqueAsPath = value; }
        }

        public List<string> unique_AS_Path
        {
            get { return Unique_AS_Path; }
            set { Unique_AS_Path = value; }
        }


    }
}
