import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

def query_dns(server, domain, index):
    start_time = time.time()
    # command = ["nslookup", domain.strip(), server]  
    command = ["dig", domain.strip(), server]

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Query {index}: {domain} -> SUCCESS")
            return time.time() - start_time
        else:
            print(f"Query {index}: FAILED (No response)")
            return 0
    except Exception as e:
        print(f"Query {index}: ERROR -> {e}")
        return 0

def run_single_domain_test(server, domain, num_threads, num_requests_per_thread):
    results = {"success": 0, "failures": 0, "durations": []}

    def execute_query(index):
        for request_num in range(num_requests_per_thread):
            duration = query_dns(server, domain, f"{index}-{request_num+1}")
            if duration > 0:
                results["durations"].append(duration)
                results["success"] += 1
            else:
                results["failures"] += 1

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(execute_query, i+1) for i in range(num_threads)]

    
    total_requests = results["success"] + results["failures"]
    print(f"\n**Resultados para {domain}:**")
    print(f"Total de consultas: {total_requests}")
    print(f"Sucesso: {results['success']}")
    print(f"Falhas: {results['failures']}")
    if results["durations"]:
        print(f"Maior tempo de requisição: {max(results['durations']):.2f} segundos")
        print(f"Menor tempo de requisição: {min(results['durations']):.2f} segundos")
        print(f"Tempo médio de requisição: {sum(results['durations']) / len(results['durations']):.2f} segundos")

def run_multi_domain_test(server, domains, num_threads, num_requests_per_thread):
    
    results = {domain: {"success": 0, "failures": 0, "durations": []} for domain in domains}

    def execute_query(index, domain):
        for request_num in range(num_requests_per_thread):
            duration = query_dns(server, domain, f"{index}-{request_num+1}")
            if duration > 0:
                results[domain]["durations"].append(duration)
                results[domain]["success"] += 1
            else:
                results[domain]["failures"] += 1

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(execute_query, i+1, domain): domain for i, domain in enumerate(domains)}


    print("\n### Teste concluído ###")
    for domain, stats in results.items():
        total_requests = stats["success"] + stats["failures"]
        print(f"\n **Resultados para {domain}:**")
        print(f"Total de consultas: {total_requests}")
        print(f"Sucesso: {stats['success']}")
        print(f"Falhas: {stats['failures']}")
        if stats["durations"]:
            print(f"Maior tempo de requisição: {max(stats['durations']):.2f} segundos")
            print(f"Menor tempo de requisição: {min(stats['durations']):.2f} segundos")
            print(f"Tempo médio de requisição: {sum(stats['durations']) / len(stats['durations']):.2f} segundos")

if __name__ == "__main__":
    dns_server = input("Insira o endereço IP do Servidor DNS: ")

    multi_domains = input("Você deseja fazer requisições de vários? (s/n): ").strip().lower()
    if multi_domains == 's':
        path = input("Insira o caminho para o arquivo dos domínios: ")
        with open(path, "r") as file:
            domains = [d.strip() for d in file.readlines() if d.strip()]
        
        threads = int(input("Quantidade de threads (default = 100): ") or 100)
        requests_per_thread = int(input("Requisições por thread (default = 100): ") or 100)

        run_multi_domain_test(dns_server, domains, threads, requests_per_thread)

    else:
        test_domain = input("Insira o Domínio a ser testado: ").strip()
        threads = int(input("Quantidade de threads (default = 100): ") or 100)
        requests_per_thread = int(input("Requisições por thread (default = 100): ") or 100)

        run_single_domain_test(dns_server, test_domain, threads, requests_per_thread)
