using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Text.RegularExpressions;

namespace ConsoleApplication1
{

    //public partial class Program
    //{


    //    int MaxEditDistnace(string [] a)
    //    {
    //        int[,] MeshMatrix = new int[a.Length, a.Length];

    //        //break AS-PATH to a list of strings
    //        List<string []> AsPathList = new List<string []>();
    //        for (int i=0;i<a.Length;i++)
    //        {
    //            AsPathList[i] = a[i].Split(' ');
    //        }


    //        for (int i = 0; i < a.Length; i++)
    //        {
    //            for (int j = 0; i < a.Length; i++)
    //            {

    //                MeshMatrix[i, j] = EditDistance(AsPathList[i], AsPathList[j]);
    //            }
    //        }


    //        return MeshMatrix[0, 0];
    //    }











    //    int EditDistance(string [] a, string [] b)
    //    {
    //        //List<string> Unique = new List<string>();
    //        ////string [] Unique;

    //        //foreach (string temp in a)
    //        //    if (Unique.Contains(temp) == false)
    //        //        Unique.Add(temp);

    //        //foreach (string temp in b)
    //        //    if (Unique.Contains(temp) == false)
    //        //        Unique.Add(temp);



    //        // for all i and j, d[i,j] will hold the Levenshtein distance between
    //        // the first i characters of s and the first j characters of t;
    //        // note that d has (m+1)x(n+1) values
    //        //declare int d[0..m, 0..n]
    //        int[,] EditDistanceArray = new int[a.Length, b.Length];
    //        //for i from 0 to m
    //        //  d[i, 0] := i // the distance of any first string to an empty second string
    //        //for j from 0 to n
    //        //  d[0, j] := j // the distance of any second string to an empty first string
    //        for (int i = 0; i < a.Length; i++)
    //            EditDistanceArray[i, 0] = i;
    //        for (int j = 0; j < b.Length; j++)
    //            EditDistanceArray[0, j] = j;

    //        //for j from 1 to n
    //        //{
    //        //  for i from 1 to m
    //        //  {
    //        //    if s[i] = t[j] then  
    //        //      d[i, j] := d[i-1, j-1]       // no operation required
    //        //    else
    //        //      d[i, j] := minimum
    //        //                 (
    //        //                   d[i-1, j] + 1,  // a deletion
    //        //                   d[i, j-1] + 1,  // an insertion
    //        //                   d[i-1, j-1] + 1 // a substitution
    //        //                 )
    //        //  }
    //        //}
    //        for (int i = 0; i < a.Length; i++)
    //        {
    //            for (int j = 0; j < b.Length; j++)
    //            {
    //                if (a[i] == b[j])
    //                    EditDistanceArray[i, j] = EditDistanceArray[i - 1, j - 1];
    //                else
    //                    EditDistanceArray[i, j] = Math.Min(
    //                        EditDistanceArray[i - 1, j] + 1,
    //                        Math.Min(
    //                            EditDistanceArray[i, j - 1] + 1,
    //                            EditDistanceArray[i - 1, j - 1] + 1)
    //                        );
    //            }
    //        }


    //        //return d[m,n]
    //        return EditDistanceArray[a.Length - 1, b.Length - 1];
    //    }
    //}
}