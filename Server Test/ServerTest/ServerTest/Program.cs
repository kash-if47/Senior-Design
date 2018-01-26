using System;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using System.Text;



    public static int Main(String[] args)
    {
    Socket soc = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
    IPHostEntry ipHostInfo = Dns.GetHostEntry(Dns.GetHostName());
    System.Net.IPAddress ipAdd = ipHostInfo.AddressList[0];
    System.Net.IPEndPoint remoteEP = new IPEndPoint(ipAdd, 3456);
    soc.Connect(remoteEP);
    byte[] byData = System.Text.Encoding.ASCII.GetBytes("un:" + "test1" + ";pw:" + "Test2");
    soc.Send(byData);
    return 0;
    }
}