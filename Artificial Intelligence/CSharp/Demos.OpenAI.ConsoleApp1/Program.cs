using Azure.AI;
using Azure.AI.OpenAI;
using OpenAI.Chat;
using System.ClientModel;
using System.Text;
using System.Text.Json;
using Newtonsoft.Json;
using System.Net.Http.Json;

namespace Demos.OpenAI.ConsoleApp1
{
    internal class Program
    {
        static string endopoint = "<endpoint>";
        static string apyKey = "<key>";

        static void Main(string[] args)
        {
            BasicChatHttp();
        }

        static void BasicChat()
        {
            var credential = new ApiKeyCredential(apyKey);
            var client = new AzureOpenAIClient(new Uri(endopoint), credential);

            var chat = client.GetChatClient("gpt-35-turbo-16k");

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Gray;
            
            Console.Write("Envia un mensaje a ChatGPT: ");
            string? message = Console.ReadLine();

            var options = new ChatMessage[]
            {
                new UserChatMessage(message)
            };

            var response = chat.CompleteChat(options);

            Console.ForegroundColor = ConsoleColor.Yellow;
            foreach(var content in response.Value.Content)
                Console.WriteLine(content.Text + Environment.NewLine);
        }
        
        static void BasicChatHttp()
        {
            string url = $"{endopoint}/openai/deployments/gpt-35-turbo-16k/chat/completions?api-version=2024-08-01-preview";
            HttpClient client = new HttpClient();

            client.DefaultRequestHeaders.Add("api-key", apyKey);

            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Gray;

            Console.Write("Envia un mensaje a ChatGPT: ");
            string? message = Console.ReadLine();

            var data = new
            {
                messages = new[] 
                {
                    new  { role = "user", content = message }
                }
            };

            var json = JsonConvert.SerializeObject(data);
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            var response = client.PostAsync(url, content).Result;
            var result = response.Content.ReadAsStringAsync().Result;

            var objResult = JsonConvert.DeserializeObject<dynamic>(result);

            Console.ForegroundColor = ConsoleColor.Yellow;
            Console.WriteLine(objResult.choices[0].message.content);
        }
    }
}
