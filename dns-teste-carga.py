import subprocess
import threading
import time

def query_dns(server, domain, index, recursive):
    start_time = time.time()
    
    # Adjust command based on recursion choice
    command = ["dig", domain, "@"+server]
    if recursive:
        command.append("+trace")  # Enables recursive query tracing

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stdout.strip()
        if output:
            print(f"Query {index}: {domain} -> SUCCESS")
        else:
            print(f"Query {index}: FAILED (No response)")
    except Exception as e:
        print(f"Query {index}: ERROR -> {e}")

    end_time = time.time()
    return end_time - start_time

def run_load_test(server, domain, num_threads, num_requests_per_thread, recursive):
    threads = []
    total_requests = num_threads * num_requests_per_thread
    successful_queries = 0
    failed_queries = 0

    def execute_queries():
        nonlocal successful_queries, failed_queries
        for i in range(num_requests_per_thread):
            duration = query_dns(server, domain, i + 1, recursive)
            if duration > 0:
                successful_queries += 1
            else:
                failed_queries += 1

    for _ in range(num_threads):
        t = threading.Thread(target=execute_queries)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"\n✅ Teste concluído com {total_requests} consultas.")
    print(f"✔️ Consultas bem-sucedidas: {successful_queries}")
    print(f"❌ Consultas falhadas: {failed_queries}")

if __name__ == "__main__":
    dns_server = input("Insira o endereço IP do Servidor DNS: ")
    test_domain = input("Insira o Dominio a ser testado: ")
    threads = int(input("Insira a quantidade de threads a serem usadas no teste (default = 100): ") or 100)
    requests_per_thread = int(input("Insira a quantidade de requisicoes por thread a serem usadas no teste (default = 100): ") or 100)
    recursive_option = input("Deseja realizar consultas recursivas? (s/n): ").strip().lower() == 's'

    run_load_test(dns_server, test_domain, threads, requests_per_thread, recursive_option)