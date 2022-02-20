using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Text.RegularExpressions;


namespace ConsoleApplication1
{
    /// <summary>
    /// The main class that contains a static main methods
    /// </summary>
    class Program
    {
        /// <summary>
        /// The main function is the starting point for the compiler to start compiling the code
        /// </summary>
        /// <param name="args"> The argument list that the user might provide to the main</param>
        static void Main(string[] args)
        {
            
            List<pins> PINS = new List<pins>();
			String file_name = "DUMP";
            int brojac = 0;


            // varijabla koju cemo koristiti, choose FROM AS
            //String from_parametar = "192.65.184.3";
            List<bgp_updates> BGP_UPDATES = new List<bgp_updates>();
            {
                // This block is to force the garbage collector get rid of Bgp_Messages_text varibale                

                ////////////////////
                //////Main loop/////
                ////////////////////

                //Parse the inpute file to bgp_updates object so all the BGP update messages will be extracted
                //file_name = args[0];
                StreamReader streamReader = new StreamReader(file_name);
                //StreamReader streamReader = new StreamReader(args[0]);
                string text = "";
                String line;
                bool ParsingFlag = false;
                bool ProcessingFlag = false;

                
                //////////////////////////
                //////Parsing  loop///////                
                //////////////////////////                
                while ((line = streamReader.ReadLine()) != null)
                {
                    if (line.Contains("TIME") == true || ParsingFlag == true)
                    {
                        //termination
                        if (line == "")
                        {
                            ParsingFlag = false; //Set the parsing flag to OFF
                            ProcessingFlag = true; //Set the processing flag to ON
                        }
                        else//parsing
                        {
                            ParsingFlag = true; //Set the parsing flag to ON
                            text += line + "\n";
                        }
                    }

                    if (ProcessingFlag == true)
                    {
                        //Ignore OPEN and KEEPALIVE messeges 
                        if (text.Contains("PARAMETER") == false && text.Contains("KEEPALIVE") == false && text.Contains("OPEN") == false && text.Contains("STATE") == false)
                        {

                            bgp_updates item = new bgp_updates();
                            string[] temp_array = text.Split(new string[] { "\n" }, StringSplitOptions.None);
                            
                            //Get the time 
                            temp_array[0] = temp_array[0].Trim();
                            //int Years = (int.Parse((temp_array[0].Split(' ')[1])));
                            string[] line_array = temp_array[0].Split(' ');

                            int Years = (int.Parse((line_array[1].Split('-')[0])));
                            int Months = (int.Parse((line_array[1].Split('-')[1])));
                            int Days = (int.Parse((line_array[1].Split('-')[2])));
                            int Hours = (int.Parse((line_array[2].Split(':')[0])));
                            int Miniutes = (int.Parse((line_array[2].Split(':')[1])));
                            int Seconds = (int.Parse((line_array[2].Split(':')[2])));

                            /*
                            int Years = (int.Parse((temp_array[0].Split(' ')[1])));
                            int Months = (int.Parse((temp_array[0].Split(' ')[2])));
                            int Days = (int.Parse((temp_array[0].Split(' ')[3])));
                            int Hours = (int.Parse((temp_array[0].Split(' ')[4].Split(':')[0])));
                            int Miniutes = (int.Parse((temp_array[0].Split(' ')[4].Split(':')[1])));
                            int Seconds = (int.Parse((temp_array[0].Split(' ')[4].Split(':')[2])));
                            */
                            DateTime date1 = new DateTime(Years, Months, Days, Hours, Miniutes, Seconds);
                            item.date = date1;
                            
                            item.sIZE = 0;
                            foreach (string temp in temp_array)
                            {
                                if (temp.Contains("AS_PATH"))
                                    item.as_path = temp.Split(':')[1].Trim();
                                if (temp.Contains("ORIGIN"))
                                    item.origin = temp.Split(':')[1].Trim();
                                if (temp.Contains("PACKET TYPE"))
                                    item.type = temp.Split(':')[1].Trim();
                                if (temp.Contains("FROM"))
                                    item.from = temp.Split(':')[1].Trim();
                                if (temp.Contains("TO:"))
                                    item.to = temp.Split(':')[1].Trim();
                                if (temp.Contains("NEXT_HOP"))
                                    item.Next_Hop = temp.Split(':')[1].Trim();
                                if (temp.Contains("ANNOUNCED")) { 
                                    item.Announced.Add((temp.Split(':')[1].Trim()).Split('/')[0]);
                                    brojac++;
                                }
                                if (temp.Contains("WITHDRAWN"))
                                    item.WITHDRAWn.Add((temp.Split(':')[1].Trim()).Split('/')[0]);
                              //  if (temp.Contains("ORIGIN"))
                              //      item.WITHDRAWn.Add((temp.Split(':')[1].Trim()).Split('/')[0]); bug!
                                if (temp.Contains("COMMUNITIES"))
                                {
                                    string[] stringSeparators = new string[] { "COMMUNITIES:" };
                                    item.cOMMUNITY_ATTRIBUTTES = temp.Split(stringSeparators, StringSplitOptions.None)[1].Trim();
                                }

                                //for getting KEEPALIVE + UPDATE+ OPEN+ NOTIFICATION
                                if (temp.Contains("BGP"))
                                {
                                    string[] stringSeparators = new string[] { "TYPE:" };
                                    item.type = temp.Split(stringSeparators, StringSplitOptions.None)[1].Trim();
                                }
                                item.sIZE += temp.Length;
                            }//end of for loop
                            
                            //exclude messages that dont have needed FROM, comment out if statement if needed all messages
                            //dio koda gdje cemo iskljuciti poruke koje nemaju odredjenu FROM adresu
                            //if (item.from == from_parametar)
                                BGP_UPDATES.Add(item);
                            Console.WriteLine("1: " + "BGP Update msg date" + item.date + ". " + BGP_UPDATES.Count + " Have been parsed.");
                        }//end of if statement

                        text = "";//reset next bgp msg
                        ProcessingFlag = false; //Set the processing flag to OFF
                    }

                }
                //continue
                streamReader.Close();
            }//To force the garbage collector get rid of Bgp_Messages_text

            int CounterOfParsedMessages = 0;
            bool flag_doitonce = true;//enable the searching for one coutn pins 

            ////////////////////////////////////
            //Big Processing Loop Compute pins//
            ////////////////////////////////////
            int brojko = 0;
            foreach (bgp_updates x in BGP_UPDATES)
            {
                pins item = new pins();//Will be added later to PINS[]
                item.time = x.date;
                //first miniute
                if (x.date.Second == 59 && x.date.Hour == 24 && x.date.Minute == 59)
                    item.time = x.date;
               
                if (x.date.Hour == 0 && x.date.Minute == 9)
                {
                    Console.WriteLine("test");
                    brojko += x.Announced.Count();
                    //Console.WriteLine("Annouced broj" + x.Announced);
                    Console.WriteLine("Kumulativno: " + brojko);

                }
                    
                if (PINS.Count == 0)
                {
                    PINS.Add(item);
                    //for any new feature add it here:
                    if (x.Announced.Count != 0)
                    {
                        PINS[0].NumberofAnnouncments += 1;
                        PINS[0].NumberOfAnnouncedPrefixes += x.Announced.Count;
                        PINS[0].NumberofUpdates += 1;
                    }
                    if (x.WITHDRAWn.Count != 0)
                    {
                        PINS[0].NumberofWithdrawals += 1;
                        PINS[0].NumberOfwithdrawnsPrefixes += x.WITHDRAWn.Count;
                        PINS[0].NumberofUpdates += 1;
                    }

                    //AS PATH                    
                    if (x.as_path != null)
                    {
                        PINS[0].AvgASPath = x.as_path.Split(' ').Length;
                        PINS[0].count_as = 1;
                        PINS[0].MaxASPath = x.as_path.Split(' ').Length; ;
                        PINS[0].AvgUniqueASPath = x.as_path.Split(' ').Length;
                        PINS[0].maxUniqueASPath = x.as_path.Split(' ').Length;
                        //PINS[0].implicitWithdrawals = 1;// will be solved later
                    }
                    else
                    {
                        PINS[0].AvgASPath = 0;
                        PINS[0].MaxASPath = 0;
                        PINS[0].AvgUniqueASPath = 0;
                        PINS[0].maxUniqueASPath = 0;
                    }

                    //ORIGIN
                    if (x.origin == "EGP")
                        PINS[0].numberOfEGP = 1;
                    else if (x.origin == "Incomplete")
                        PINS[0].numberOfIncomplete = 1;
                    else if (x.origin == "IGP") // used else if used to be else only
                        PINS[0].numberOfIGP = 1;

                    //TYPE
                    if (x.type == "UPDATE")
                        PINS[0].numberOfUPDATEMessages = 1;
                    else if (x.type == "KEEPALIVE")
                        PINS[0].numberOfKeepAliveMessages = 1;
                    else if (x.type == "NOTIFICATION")
                        PINS[0].numberOfNOTIFICATIONMessages = 1;
                    else if (x.type == "OPEN")
                        PINS[0].numberOfOPENMessages = 1;

                    //Size
                    PINS[0].AVGSize = x.sIZE;

                    //BGP Announcement Types 
                    //nothing!
                    PINS[0].pinsBGPUpdates.Add(x);
                    PINS[0].count = 1;
                }


                ////////////////////////
                //Other miniutes
                else if (PINS[PINS.Count - 1].time.Hour == item.time.Hour && PINS[PINS.Count - 1].time.Minute == item.time.Minute)
                { //for any new feature add it here:

                    if (x.Announced.Count != 0)
                    {
                        if (x.date.Hour == 9 && x.date.Minute == 55)
                            Console.WriteLine("Stop");
                        PINS[PINS.Count - 1].NumberofAnnouncments += 1;
                        PINS[PINS.Count - 1].NumberOfAnnouncedPrefixes += x.Announced.Count;
                        if (x.date.Hour == 9 && x.date.Minute == 55)
                            Console.WriteLine("INterni: " + PINS[PINS.Count - 1].NumberOfAnnouncedPrefixes);
                        PINS[PINS.Count - 1].NumberofUpdates += 1;
                    }
                    if (x.WITHDRAWn.Count != 0)
                    {
                        PINS[PINS.Count - 1].NumberofWithdrawals += 1;
                        PINS[PINS.Count - 1].NumberOfwithdrawnsPrefixes += x.WITHDRAWn.Count;
                        PINS[PINS.Count - 1].NumberofUpdates += 1;
                    }

                    //AS PATH
                    if (x.as_path != null)
                    {
                        PINS[PINS.Count - 1].AvgASPath += x.as_path.Split(' ').Length;
                        PINS[PINS.Count - 1].count_as += 1;
                        if (x.as_path.Split(' ').Length > PINS[PINS.Count - 1].MaxASPath)
                            PINS[PINS.Count - 1].MaxASPath = x.as_path.Split(' ').Length;
                    }
                    //Unique AS PATH
                    if (x.as_path != null)
                    {
                        //solve for the first item
                        if (PINS[PINS.Count - 1].unique_AS_Path.Count == 0)
                        {
                            PINS[PINS.Count - 1].unique_AS_Path.Add(x.as_path);
                            PINS[PINS.Count - 1].count_unique_as += 1;
                        }
                        else//for other item...
                        {   //Check  if the AS PATH is not there!
                            if (PINS[PINS.Count - 1].unique_AS_Path.Contains(x.as_path) == false)
                            {
                                PINS[PINS.Count - 1].unique_AS_Path.Add(x.as_path);
                                PINS[PINS.Count - 1].count_unique_as += 1;
                            }

                            //MaxUniqueAsPath
                            if (PINS[PINS.Count - 1].unique_AS_Path[PINS[PINS.Count - 1].unique_AS_Path.Count - 1].Split(' ').Length > PINS[PINS.Count - 1].maxUniqueASPath)
                                PINS[PINS.Count - 1].maxUniqueASPath = x.as_path.Split(' ').Length;
                        }
                    }
                    //Duplicate BGP packets                                 
                    PINS[PINS.Count - 1].pinsBGPUpdates.Add(x);

                    //ORIGIN
                    if (x.origin == "EGP")
                        PINS[PINS.Count - 1].numberOfEGP += 1;
                    else if (x.origin == "Incomplete")
                        PINS[PINS.Count - 1].numberOfIncomplete += 1;
                    else if (x.origin == "IGP") // used else if used to be else only
                        PINS[PINS.Count - 1].numberOfIGP += 1;
                    //TYPE
                    if (x.type == "UPDATE")
                        PINS[PINS.Count - 1].numberOfUPDATEMessages += 1;
                    else if (x.type == "KEEPALIVE")
                        PINS[PINS.Count - 1].numberOfKeepAliveMessages += 1;
                    else if (x.type == "NOTIFICATION")
                        PINS[PINS.Count - 1].numberOfNOTIFICATIONMessages += 1;
                    else if (x.type == "OPEN")
                        PINS[PINS.Count - 1].numberOfOPENMessages += 1;

                    //Size
                    PINS[PINS.Count - 1].AVGSize += x.sIZE;
                    PINS[PINS.Count - 1].count += 1;
                }

                //////////////////////////////////
                else if (PINS[0].time.Hour == item.time.Hour && PINS[0].time.Minute == item.time.Minute)//for those bgp messages that come late and belongs to the first pin
                { //for any new feature add it here:
                    if (x.Announced.Count != 0)
                    {
                        PINS[0].NumberofAnnouncments += 1;
                        PINS[0].NumberOfAnnouncedPrefixes += x.Announced.Count;
                        PINS[0].NumberofUpdates += 1;
                    }
                    if (x.WITHDRAWn.Count != 0)
                    {
                        PINS[0].NumberofWithdrawals += 1;
                        PINS[0].NumberOfwithdrawnsPrefixes += x.WITHDRAWn.Count;
                        PINS[0].NumberofUpdates += 1;
                    }

                    //AS PATH
                    if (x.as_path != null)
                    {
                        PINS[0].AvgASPath += x.as_path.Split(' ').Length;
                        PINS[0].count_as += 1;
                        if (x.as_path.Split(' ').Length > PINS[0].MaxASPath)
                            PINS[0].MaxASPath = x.as_path.Split(' ').Length;
                    }
                    //Unique AS PATH
                    if (x.as_path != null)
                    {
                        //solve for the first item
                        if (PINS[0].unique_AS_Path.Count == 0)
                        {
                            PINS[0].unique_AS_Path.Add(x.as_path);
                            PINS[0].count_unique_as += 1;
                        }
                        else//for other item...
                        {   //Check  if the AS PATH is not there!
                            if (PINS[0].unique_AS_Path.Contains(x.as_path) == false)
                            {
                                PINS[0].unique_AS_Path.Add(x.as_path);
                                PINS[0].count_unique_as += 1;
                            }

                            //MaxUniqueAsPath
                            if (PINS[0].unique_AS_Path[PINS[0].unique_AS_Path.Count - 1].Split(' ').Length > PINS[0].maxUniqueASPath)
                                PINS[0].maxUniqueASPath = x.as_path.Split(' ').Length;
                        }
                    }

                    //ORIGIN
                    if (x.origin == "EGP")
                        PINS[0].numberOfEGP += 1;
                    else if (x.origin == "Incomplete")
                        PINS[0].numberOfIncomplete += 1;
                    else if (x.origin == "IGP") // used else if used to be else only
                        PINS[0].numberOfIGP += 1;

                    //TYPE
                    if (x.type == "UPDATE")
                        PINS[0].numberOfUPDATEMessages = 1;
                    else if (x.type == "KEEPALIVE")
                        PINS[0].numberOfKeepAliveMessages += 1;
                    else if (x.type == "NOTIFICATION")
                        PINS[0].numberOfNOTIFICATIONMessages += 1;
                    else if (x.type == "OPEN")
                        PINS[0].numberOfOPENMessages += 1;

                    //Size
                    PINS[0].AVGSize += x.sIZE;
                    PINS[PINS.Count - 1].count += 1;
                }

                ////////////////////////
                else//Go forward to next pin 
                {
                    //TO_DO Iniliaze the first pin as pin zero...just in case there is no other pins
                    PINS.Add(item);
                  

                    //for any new feature add it here:
                    if (x.Announced.Count != 0)
                    {
                        PINS[PINS.Count - 1].NumberofAnnouncments = 1;

                        // NERMIN ISPRAVKA GRESKE U BROJANJU ANNOUCED 
                        //PINS[PINS.Count - 1].NumberOfAnnouncedPrefixes += 1;  OVA LINIJA JE BILA POGRESNA
                        PINS[PINS.Count - 1].NumberOfAnnouncedPrefixes = x.Announced.Count;  // ISPRAVLJENO NA OVO 
                        //PINS[PINS.Count - 1].NumberofUpdates = 1;
                    }
                    if (x.WITHDRAWn.Count != 0)
                    {
                        PINS[PINS.Count - 1].NumberofWithdrawals = 1;
                        // NERMIN ISPRAVKA GRESKE U BROJANJU WITHDRAWN 
                        //PINS[PINS.Count - 1].NumberOfwithdrawnsPrefixes = 1;  OVA LINIJA JE BILA POGRESNA
                        PINS[PINS.Count - 1].NumberOfwithdrawnsPrefixes = x.WITHDRAWn.Count;   // ISRAVLJENO JE NA OVO 

                        PINS[PINS.Count - 1].NumberofUpdates = 1;
                    }

                    //AS PATH                    
                    if (x.as_path != null)
                    {
                        PINS[PINS.Count - 1].AvgASPath = x.as_path.Split(' ').Length;
                        PINS[PINS.Count - 1].count_as = 1;
                        PINS[PINS.Count - 1].count_unique_as = 1;                        
                        PINS[PINS.Count - 1].MaxASPath = 1;
                        PINS[PINS.Count - 1].AvgUniqueASPath = 1;
                        PINS[PINS.Count - 1].maxUniqueASPath = 1;
                    }


                    /////////////////////////////////////////////////
                    // doooodaaajjjjjj porukuuuuuuuu
                    PINS[PINS.Count - 1].pinsBGPUpdates.Add(x);



                    //ORIGIN
                    if (x.origin == "EGP")
                        PINS[PINS.Count - 1].numberOfEGP = 1;
                    else if (x.origin == "Incomplete")
                        PINS[PINS.Count - 1].numberOfIncomplete = 1;
                    else if (x.origin == "IGP") // used else if used to be else only
                        PINS[PINS.Count - 1].numberOfIGP = 1;

                    //TYPE
                    if (x.type == "UPDATE")
                        PINS[PINS.Count - 1].numberOfUPDATEMessages = 1;
                    else if (x.type == "KEEPALIVE")
                        PINS[PINS.Count - 1].numberOfKeepAliveMessages = 1;
                    else if (x.type == "NOTIFICATION")
                        PINS[PINS.Count - 1].numberOfNOTIFICATIONMessages = 1;
                    else if (x.type == "OPEN")
                        PINS[PINS.Count - 1].numberOfOPENMessages = 1;

                    //Size
                    PINS[PINS.Count - 1].AVGSize = 1;
                    PINS[PINS.Count - 1].count = 1;
                }




                //Logging //"PINS.Count ="+PINS.Count +
                Console.WriteLine("2: " + " x.date =" + x.date + " i=" + CounterOfParsedMessages + " have been processed.");
                CounterOfParsedMessages++;
            }
            
            //////////////////////////////////////////
            //Loop to compute the Duplicate BGP packets//
            //////////////////////////////////////////
            //*****
            //****
            //***
            //**
            //*
            int CounterOfProcessedMessages = 0;
            foreach (pins pin in PINS)//for all the pins
            {
                for (int i = 0; i < pin.pinsBGPUpdates.Count-1; i++) //take 1 pin
                {
                    //                    for (int j = pin.pinsBGPUpdates.Count - 1 - i; j < pin.pinsBGPUpdates.Count; j++) //cross
                    //for (int j = 0; j <= i; j++) //cross new!
                    
                    // New Loop
                    for (int j = i+1; j < pin.pinsBGPUpdates.Count; j++) //cross
                    {
                        foreach (string plapla in pin.pinsBGPUpdates[i].Announced)
                        { 
                        
                            if (pin.pinsBGPUpdates[j].Announced.Contains(plapla))
                            {
                                
                                if (pin.pinsBGPUpdates[j].as_path == pin.pinsBGPUpdates[i].as_path)//Duplicate
                                {
                                    if (pin.pinsBGPUpdates[j].date.Hour == 0 && pin.pinsBGPUpdates[j].date.Minute == 5)
                                        Console.WriteLine("aaaaa");
                                    pin.duplicateBGPAnnouncements += 1;
                                }
                                else if (pin.pinsBGPUpdates[j].as_path != pin.pinsBGPUpdates[i].as_path)//Implicit Withdrawal
                                {
                                   
                                    pin.implicitWithdrawals += 1;
                                }

                            }
                        }
                        //Check for duplicate Withdrawals
                        foreach (string plapla in pin.pinsBGPUpdates[i].WITHDRAWn)
                            if (pin.pinsBGPUpdates[j].WITHDRAWn.Contains(plapla))
                            {
                                //New condition of same path added 
                                //dodala uslov da je i isti path
                                if (pin.pinsBGPUpdates[j].as_path == pin.pinsBGPUpdates[i].as_path)//Duplicate
                                {
                                    if (pin.pinsBGPUpdates[j].date.Hour == 0 && pin.pinsBGPUpdates[j].date.Minute == 9)
                                        Console.WriteLine("aaaaa" + pin.pinsBGPUpdates[j].WITHDRAWn + "dddd" + pin.pinsBGPUpdates[i].WITHDRAWn);
                                    pin.duplicateBGPWithdrawls += 1;
                                }
                            }
                    }
                }
                CounterOfProcessedMessages++;
                Console.WriteLine("3: " + "Duplicate for pin number: " + CounterOfProcessedMessages + " is bieng prcoessed. (" + pin.count_as + " bgp msgs)");
            }            



            //Calculate the Average AS-PATH length
            for (int i = 0; i < PINS.Count; i++)
            {
                //Fix AS-PATH sum
                //PINS[i].AvgASPath = Math.Round(PINS[i].AvgASPath / PINS[i].count);
                PINS[i].AvgASPath = Math.Ceiling((PINS[i].AvgASPath / PINS[i].count_as));//*100 to make it obvious between the AvgUniqueASPath and AvgASPath

                //Fix Unique AS-PATH count + sum
                foreach (string temp in PINS[i].unique_AS_Path)
                {
                    PINS[i].AvgUniqueASPath += temp.Split(' ').Length;
                }
                PINS[i].AvgUniqueASPath = Math.Ceiling((PINS[i].AvgUniqueASPath / PINS[i].count_unique_as));
                if (PINS[i].count != 0)
                    PINS[i].AVGSize = (int)(Math.Ceiling((PINS[i].AVGSize / PINS[i].count) * 1.0));
            }            

            
            //Compute the Max Edit distance            
            int NumberOfEditDistanceCalculatedPins = 1;
            foreach (pins temp in PINS)
            {
                //get all the as-path from each packet
                List<string> to_send = new List<string>();
                foreach (bgp_updates x1 in temp.pinsBGPUpdates)
                    // ovdje se upravlja da li ce ici dupli as path-ovi ili samo jedinstveni u razmatranje
                    if (x1.as_path != null && to_send.Contains(x1.as_path) == false)
                    {
                        //If needed NOT to consider duplicate ASs than use these two lines (comment the one below - to_send.Add(x1.as_path);) otherwise comment it out!
                        // ove dvije linije definisu da se iz as patha iskljuce duple vrijednosti 
                        //to get all unique ASs so it wont be the same as max as path length  
                        //HashSet<string> items = new HashSet<string>(x1.as_path.Split(' '));
                        //to_send.Add(String.Join(" ", items.ToArray()));

                        //If needed to consider duplicate ASs than use this otherwise comment it out!
                        //ukoliko treba da se razmatraju i duple vrijednosti iz as path-ova
                        // odkomentarisati donju liniju a zakomentarisati prethodne dvije
                        to_send.Add(x1.as_path);

                    }
                Console.WriteLine("4: " + "Computing Edit Distance for pin= " + NumberOfEditDistanceCalculatedPins + ", that contains= " + temp.count_as + " bgp msgs.");
                int[] output = MaxEditDistnace(to_send);
                temp.maximumAsPathEditDistnace = output[0];
                temp.averageAsPathEditDistnace = output[1];
                temp.minimumAsPathEditDistnace = output[2];
                NumberOfEditDistanceCalculatedPins++;
            }

            /////////////////////////
            //Writing to the stdout//
            /////////////////////////

            TextWriter streamwriter1 = new StreamWriter(file_name+ "_out.txt");
            TextWriter streamwriter2 = new StreamWriter(file_name + "_featureselection.txt");
            //TextWriter streamwriter1 = new StreamWriter(args[1]);
            //TextWriter streamwriter2 = new StreamWriter(args[1] + "_featureselection");
            for (int i = 0; i < PINS.Count; i++)
            {
                string SecondToPrint;
                if (PINS[i].time.Second < 10)
                    SecondToPrint = "0" + PINS[i].time.Second.ToString();
                else
                    SecondToPrint = PINS[i].time.Second.ToString();

                string MinuteToPrint;
                if (PINS[i].time.Minute < 10)
                    MinuteToPrint = "0" + PINS[i].time.Minute.ToString();
                else
                    MinuteToPrint = PINS[i].time.Minute.ToString();

                string HourToPrint;
                if (PINS[i].time.Hour < 10)
                    HourToPrint = "0" + PINS[i].time.Hour.ToString();
                else
                    HourToPrint = PINS[i].time.Hour.ToString();

                string output18 = ((Math.Round(PINS[i].MaxASPath) == 11) ? "1" : "0");
                string output19 = ((Math.Round(PINS[i].MaxASPath) == 12) ? "1" : "0");
                string output20 = ((Math.Round(PINS[i].MaxASPath) == 13) ? "1" : "0");
                string output21 = ((Math.Round(PINS[i].MaxASPath) == 14) ? "1" : "0");
                string output22 = ((Math.Round(PINS[i].MaxASPath) == 15) ? "1" : "0");
                string output23 = ((Math.Round(PINS[i].MaxASPath) == 16) ? "1" : "0");
                string output24 = ((Math.Round(PINS[i].MaxASPath) == 17) ? "1" : "0");
                string output25 = ((Math.Round(PINS[i].MaxASPath) == 18) ? "1" : "0");
                string output26 = ((Math.Round(PINS[i].MaxASPath) == 19) ? "1" : "0");
                string output27 = ((Math.Round(PINS[i].MaxASPath) == 20) ? "1" : "0");
                string output28 = ((Math.Round(PINS[i].maximumAsPathEditDistnace * 1.0) == 7) ? "1" : "0");
                string output29 = ((Math.Round(PINS[i].maximumAsPathEditDistnace * 1.0) == 8) ? "1" : "0");
                string output30 = ((Math.Round(PINS[i].maximumAsPathEditDistnace * 1.0) == 9) ? "1" : "0");
                string output31 = ((Math.Round(PINS[i].maximumAsPathEditDistnace * 1.0) == 10) ? "1" : "0");
                string output32 = ((Math.Round(PINS[i].maximumAsPathEditDistnace * 1.0) == 11) ? "1" : "0");
                string output33 = ((Math.Round(PINS[i].maximumAsPathEditDistnace * 1.0) == 12) ? "1" : "0");
                string output34 = ((Math.Round(PINS[i].maximumAsPathEditDistnace * 1.0) == 13) ? "1" : "0");
                string output35 = ((Math.Round(PINS[i].maximumAsPathEditDistnace * 1.0) == 14) ? "1" : "0");
                string output36 = ((Math.Round(PINS[i].maximumAsPathEditDistnace * 1.0) == 15) ? "1" : "0");
                string output37 = ((Math.Round(PINS[i].maximumAsPathEditDistnace * 1.0) == 16) ? "1" : "0");               


                /////////////////////
                /////Text format/////
                /////////////////////
                Console.WriteLine(
                    HourToPrint + MinuteToPrint + " " +//1
                    HourToPrint + " " +//2
                    MinuteToPrint + " " + //3
                    SecondToPrint + " " + //4
                    PINS[i].NumberofAnnouncments + " " +//5
                    PINS[i].NumberofWithdrawals + " " +//6                    
                    PINS[i].NumberOfAnnouncedPrefixes + " " +//7
                    PINS[i].NumberOfwithdrawnsPrefixes + " " +//8
                    PINS[i].AvgASPath + " " +//9
                    PINS[i].MaxASPath + " " +//10
                    PINS[i].AvgUniqueASPath + " " +//11
                    PINS[i].duplicateBGPAnnouncements + " " + //12
                    PINS[i].implicitWithdrawals + " " +//13
                    PINS[i].duplicateBGPWithdrawls + " " +//14
                    PINS[i].maximumAsPathEditDistnace + " " +//15
                    ((1 / (60.0 / Math.Ceiling(PINS[i].pinsBGPUpdates.Count * 1.0))).ToString() + "000").Substring(0, 3) + " " +//16                    
                    PINS[i].averageAsPathEditDistnace + " " +//17

                    output18 + " " +//18
                    output19 + " " +//19
                    output20 + " " +//20
                    output21 + " " +//21
                    output22 + " " +//22
                    output23 + " " +//23
                    output24 + " " +//24
                    output25 + " " +//25
                    output26 + " " +//26
                    output27 + " " +//27

                    output28 + " " +//28
                    output29 + " " +//29
                    output30 + " " +//30
                    output31 + " " +//31
                    output32 + " " +//32
                    output33 + " " +//33
                    output34 + " " +//34
                    output35 + " " +//35
                    output36 + " " +//36
                    output37 + " " +//37
                    PINS[i].numberOfIGP + " " + //38
                    PINS[i].numberOfEGP + " " + //39
                    PINS[i].numberOfIncomplete + " " + //40
                    PINS[i].AVGSize//45 //41
                    );//17


                /////////////////////
                //For matlab format//
                /////////////////////
                streamwriter1.WriteLine(
                    HourToPrint + MinuteToPrint + " " //1
                    + HourToPrint + " " +//2
                    MinuteToPrint + " " + //3
                    SecondToPrint + " " +//4
                    PINS[i].NumberofAnnouncments + " " + //5
                    PINS[i].NumberofWithdrawals + " " + //6
                    PINS[i].NumberOfAnnouncedPrefixes + " " + //7
                    PINS[i].NumberOfwithdrawnsPrefixes + " " +//8
                    PINS[i].AvgASPath + " " +//9
                    PINS[i].MaxASPath + " " +//10
                    PINS[i].AvgUniqueASPath + " " +//11
                    PINS[i].duplicateBGPAnnouncements + " " + //12
                    PINS[i].implicitWithdrawals + " " +//13
                    PINS[i].duplicateBGPWithdrawls + " " +//14
                    PINS[i].maximumAsPathEditDistnace + " " +//15
                    ((1 / (60.0 / Math.Ceiling(PINS[i].pinsBGPUpdates.Count * 1.0))).ToString() + "000").Substring(0, 3) + " " +//16 //4.3
                    PINS[i].averageAsPathEditDistnace + " " +//17                  

                    output18 + " " +//18
                    output19 + " " +//19
                    output20 + " " +//20
                    output21 + " " +//21
                    output22 + " " +//22
                    output23 + " " +//23
                    output24 + " " +//24
                    output25 + " " +//25
                    output26 + " " +//26
                    output27 + " " +//27
                    output28 + " " +//28
                    output29 + " " +//29
                    output30 + " " +//30
                    output31 + " " +//31
                    output32 + " " +//32
                    output33 + " " +//33
                    output34 + " " +//34
                    output35 + " " +//35
                    output36 + " " +//36
                    output37 + " " +//37
                    PINS[i].numberOfIGP + " " + //38
                    PINS[i].numberOfEGP + " " + //39
                    PINS[i].numberOfIncomplete + " " +//40                

                     PINS[i].AVGSize//45 //41
                    );

                ////////////////////////////
                //Feature selection Format//
                ////////////////////////////
                if (i <= 800)
                    streamwriter2.Write("-1 ");
                else
                    streamwriter2.Write("1 ");

                streamwriter2.WriteLine(
                  "1:" +
                  PINS[i].NumberofAnnouncments + " 2:" + //1
                  PINS[i].NumberofWithdrawals + " 3:" + //2
                  PINS[i].NumberOfAnnouncedPrefixes + " 4:" + //3
                  PINS[i].NumberOfwithdrawnsPrefixes + " 5:" +//4
                  PINS[i].AvgASPath + " 6:" +//5
                  PINS[i].MaxASPath + " 7:" +//6
                  PINS[i].AvgUniqueASPath + " 8:" +//7
                  PINS[i].duplicateBGPAnnouncements + " 9:" + //8
                  PINS[i].implicitWithdrawals + " 10:" +//9
                  PINS[i].duplicateBGPWithdrawls + " 11:" +//10
                  PINS[i].maximumAsPathEditDistnace + " 12:" +//11
                  ((1 / (60.0 / Math.Ceiling(PINS[i].pinsBGPUpdates.Count * 1.0))).ToString() + "000").Substring(0, 3) + " 13:" +//12
                  PINS[i].averageAsPathEditDistnace + " 14:" +//13
                     output18 + " 15:" +//14
                     output19 + " 16:" +//15
                     output20 + " 17:" +//16
                     output21 + " 18:" +//17
                     output22 + " 19:" +//18
                     output23 + " 20:" +//19
                     output24 + " 21:" +//20
                     output25 + " 22:" +//21
                     output26 + " 23:" +//22
                     output27 + " 24:" +//23
                     output28 + " 25:" +//24
                     output29 + " 26:" +//25
                     output30 + " 27:" +//26
                     output31 + " 28:" +//27
                     output32 + " 29:" +//28
                     output33 + " 30:" +//29
                     output34 + " 31:" +//30
                     output35 + " 32:" +//31
                     output36 + " 33:" +//32
                     output37 + " 34:" +//33
                     PINS[i].numberOfIGP + " 35:" + //34
                     PINS[i].numberOfEGP + " 36:" + //35
                     PINS[i].numberOfIncomplete + " 37:" + //36
                     PINS[i].AVGSize//41 //37
                  );
            }
            streamwriter1.Close();
            streamwriter2.Close();
        }//end of main



        /// <summary>
        /// This function compute the Maximum Edit distance from a collection of edit distances
        /// </summary>
        /// <param name="a">It is a list of edit distnaces</param>
        /// <returns></returns>
        public static int[] MaxEditDistnace(List<string> a)
        {
            //int[,] MeshMatrix = new int[a.Count, a.Count];
            int max = 0;
            int min = 1000;
            int sum = 0;
            //break AS-PATH to a list of strings
            List<string[]> AsPathList = new List<string[]>();
            foreach (string x in a)
            {
                AsPathList.Add(x.Split(' '));
            }
            // Added variable to use for counting number of comparisons in a loop
            // dodala varijablu koju cu koristiti za brojanje poredjenja u petlji
            int brojac = 0;

            for (int i = 0; i < a.Count; i++)
            //for (int i = 0; i < a.Count-1; i++)
                {
                //for (int j = a.Count - 1 - i; j < a.Count; j++)//wrong
                 for (int j = 0; j <= i; j++)
                //for (int j = i+1; j < a.Count ; j++)
                {
                    int current = EditDistance(AsPathList[i], AsPathList[j]);
                    sum += current;
                    if (current > max)
                        max = current;
                    if (current < min && i != j)//Avoid zero distnace
                        min = current;
                      
                    // Increase the counter unless comparing two same messages i=j
                    // povecaj brojac poredjenja osim u slucaju kada se porede dvije iste poruke i=j
                    if (i!= j)
                        brojac++;           
                }
            }

            int[] temp = new int[3];
            temp[0] = max;

            // Calculating average edit distance with square - wrong!
            // izracun prosjecnog edit distance patha sa kvadratom 
            //temp[1] = (int)(Math.Ceiling((sum * 1.0) / (a.Count * a.Count)));

            // Calculating average edit distance by computing sum of all edit distances and dividing it by number of comparisons
            // izracun dijeljenjem sume svih path-ova kroz broj poredjenja
            temp[1] = (int)(Math.Ceiling((sum * 1.0) / (brojac)));
            temp[2] = min;

            //   return MeshMatrix.Cast<int>().Max(); 
            return temp;
        }

        /// <summary>
        /// This function calculate the edit distance between two AS-PATHs
        /// </summary>
        /// <param name="a">The first AS-PATH</param>
        /// <param name="b">The Second AS-PATH</param>
        /// <returns>It returns an integer with the vaule if the edit distance</returns>
        public static int EditDistance(string[] a, string[] b)
        {
            // for all i and j, d[i,j] will hold the Levenshtein distance between
            // the first i characters of s and the first j characters of t;
            // note that d has (m+1)x(n+1) values
            //declare int d[0..m, 0..n]
            int[,] EditDistanceArray = new int[a.Length + 1, b.Length + 1];
            //for i from 0 to m
            //  d[i, 0] := i // the distance of any first string to an empty second string
            //for j from 0 to n
            //  d[0, j] := j // the distance of any second string to an empty first string
            for (int i = 0; i < a.Length + 1; i++)
                EditDistanceArray[i, 0] = i;
            for (int j = 0; j < b.Length + 1; j++)
                EditDistanceArray[0, j] = j;

            for (int i = 1; i <= a.Length; i++)
            {
                for (int j = 1; j <= b.Length; j++)
                {
                    //if (a[i] == b[j] && i == 0 && j == 0)
                    //    EditDistanceArray[i, j] = 0;
                    if (a[i - 1] == b[j - 1])
                        EditDistanceArray[i, j] = EditDistanceArray[i - 1, j - 1];
                    else
                        EditDistanceArray[i, j] = Math.Min(
                            EditDistanceArray[i - 1, j] + 1,
                            Math.Min(
                                EditDistanceArray[i, j - 1] + 1,
                                EditDistanceArray[i - 1, j - 1] + 1)
                            );
                }
            }

            //return d[m,n]
            return EditDistanceArray[a.Length, b.Length];
        }
    }
}