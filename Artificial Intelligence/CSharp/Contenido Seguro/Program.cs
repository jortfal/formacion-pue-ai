using Azure.AI.ContentSafety;
using Azure;
using Newtonsoft.Json;
using System.Text;

namespace Contenido_Seguro
{
    class Program
    {
        private static string url = "<endpoint>";
        private static string clave = "<key1 or key2>";

        /// <summary>
        /// Método Principal
        /// </summary>
        /// <param name="args"></param>
        static void Main(string[] args)
        {
            string texto = "Eres un poco idiota ...";
            RunREST(texto);
        }

        /// <summary>
        /// Utilización del servicio de Seguridad del Contenido mediante API Rest
        /// </summary>
        /// <param name="texto"></param>
        public static void RunREST(string texto)
        {
            HttpClient http = new();
            http.DefaultRequestHeaders.Add("Ocp-Apim-Subscription-Key", clave);

            string endpoint = $"{url}/contentsafety/text:analyze?api-version=2023-10-01";
            
            var playload = new { text = texto };
            string jsonPlayLoad = JsonConvert.SerializeObject(playload);
            StringContent requestData = new StringContent(jsonPlayLoad, Encoding.UTF8, "application/json");

            var response = http.PostAsync(endpoint, requestData).Result;
            if(response.IsSuccessStatusCode)
            {
                Console.WriteLine(response.Content.ReadAsStringAsync().Result);
            }
            else Console.WriteLine($"Error {(int)response.StatusCode}: {response.StatusCode}");
        }

        /// <summary>
        /// Utilización del servicio de Seguridad del Contenido mediante SDK
        /// </summary>
        /// <param name="texto"></param>
        public static void RunSDK(string texto)
        {
            var cliente = new ContentSafetyClient(new Uri(url), new AzureKeyCredential(clave));    
            var consulta = new AnalyzeTextOptions(texto);

            try
            {
                var respuesta = cliente.AnalyzeText(consulta);

                foreach (var item in respuesta.Value.CategoriesAnalysis)
                {
                    Console.WriteLine($"{item.Category}: {item.Severity}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }
    }
}