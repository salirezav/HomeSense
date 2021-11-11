# 1 "c:\\Users\\salir\\Desktop\\home automation\\esp01 relay\\esprelay.ino"
# 2 "c:\\Users\\salir\\Desktop\\home automation\\esp01 relay\\esprelay.ino" 2

const char* ssid = "Big Brother 2G"; // fill in here your router or wifi SSID
const char* password = "WhyAreYouAsking?"; // fill in here your router or wifi password

WiFiServer server(80);

void setup()
{
  Serial.begin(115200); // must be same baudrate with the Serial Monitor

  pinMode(0 /* relay connected to  GPIO0*/,0x01);
  digitalWrite(0 /* relay connected to  GPIO0*/, 0x0);

  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  // Start the server
  server.begin();
  Serial.println("Server started");

  // Print the IP address
  Serial.print("Use this URL to connect: ");
//   Serial.print("https://192.168.0.178/");
  Serial.print(WiFi.localIP());
  Serial.println("/");

}

void loop()
{
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client)
  {
    return;
  }

  // Wait until the client sends some data
  Serial.println("new client");
  while(!client.available())
  {
    delay(1);
  }

  // Read the first line of the request
  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();

  // Match the request
  int value = 0x0;
  if (request.indexOf("/RELAY=ON") != -1)
  {
    Serial.println("RELAY=ON");
    digitalWrite(0 /* relay connected to  GPIO0*/,0x0);
    value = 0x0;
  }
  if (request.indexOf("/RELAY=OFF") != -1)
  {
    Serial.println("RELAY=OFF");
    digitalWrite(0 /* relay connected to  GPIO0*/,0x1);
    value = 0x1;
  }

  // Return the response
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println(""); //  this is a must
  client.println("<!DOCTYPE HTML>");
  client.println("<html>");
  client.println("<head><title>ESP8266 RELAY Control</title></head>");
  client.print("Relay is now: ");

  if(value == 0x1)
  {
    client.print("OFF");
  }
  else
  {
    client.print("ON");
  }
  client.println("<br><br>");
  client.println("Turn <a href=\"/RELAY=OFF\">OFF</a> RELAY<br>");
  client.println("Turn <a href=\"/RELAY=ON\">ON</a> RELAY<br>");
    client.println("</html>");

  delay(1);
  Serial.println("Client disonnected");
  Serial.println("");
}
