import numpy as np
import random
import timeit
import matplotlib.pyplot as plt
from memory_profiler import memory_usage

def find_flag_path():
    # Server web
    server_web = {
        'index.html': ['menu.html', 'view.html', 'contact.html', 'about.html', 'faq.html', 'news.html', 'privacy.html', ],
        'menu.html': ['pictures.html', 'data.html', 'faq.html', 'about.html', 'news.html', 'privacy.html'],
        'pictures.html': ['index.html', 'menu.html', 'news.html', 'privacy.html', 'data.html'],
        'data.html': ['menu.html', 'faq.html', 'about.html', 'news.html', 'privacy.html', 'view.html'],
        'view.html': ['index.html', 'menu.html', 'news.html', 'privacy.html'],
        'contact.html': ['location.html', 'about.html', 'news.html', 'privacy.html'],
        'location.html': ['index.html', 'menu.html', 'about.html', 'news.html', 'privacy.html'],
        'about.html': ['menu.html', 'contact.html', 'location.html', 'faq.html', 'search.html', 'news.html', 'privacy.html'],
        'faq.html': ['menu.html', 'about.html', 'news.html', 'privacy.html'],
        'search.html': ['index.html', 'menu.html', 'pictures.html', 'data.html', 'view.html', 'contact.html', 'location.html', 'about.html', 'faq.html', 'news.html', 'privacy.html', 'sixth.html'],
        'news.html': ['index.html', 'menu.html', 'privacy.html', 'contact.html', 'location.html', 'about.html', 'faq.html'],
        'privacy.html': ['index.html', 'menu.html', 'search.html', 'news.html', 'contact.html', 'location.html', 'about.html', 'faq.html'],
        'sixth.html': ['index.html', 'menu.html', 'pictures.html', 'data.html', 'view.html', 'search.html']
    }

    # Posizione della bandiera
    flag_file = 'sixth.html'
    
    # Posizione della bandiera random ma diverso da index
    #flag_file = random.choice(list(server_web.keys()))
    while flag_file == 'index.html':
      flag_file = random.choice(list(server_web.keys()))

    # Mappatura dei file agli indici
    file_indices = {file: i for i, file in enumerate(server_web)}

    # Mappatura degli indici ai file
    index_files = {i: file for file, i in file_indices.items()}

    # Numero di file
    n_files = len(server_web)

    # Inizializzazione della Q-table
    Q = np.zeros((n_files, n_files))

    # Parametri per l'apprendimento
    alpha = 0.1
    gamma = 0.99
    epsilon = 0.1
    n_episodes = 1000

    iterazioni = 0 # inizializza il contatore delle iterazioni

    for _ in range(n_episodes):

        # Calcola il tasso di apprendimento e il tasso di esplorazione
        apprendimento = alpha * 100
        esplorazione = epsilon * 100
        #print(f"Tasso di apprendimento: {apprendimento:.2f}%, Tasso di esplorazione: {esplorazione:.2f}%")
        
        # Inizia dall'index.html
        state = file_indices['index.html']

        while index_files[state] != flag_file:
            # Azioni possibili
            actions = [file_indices[file] for file in server_web[index_files[state]]]

            if not actions:  # Aggiungi questa condizione
                break

            # Scegli un'azione usando l'epsilon-greedy
            if random.uniform(0, 1) < epsilon:
                action = random.choice(actions)
            else:
                action = actions[np.argmax(Q[state, actions])]

            # Trova il file successivo
            next_file = index_files[action]

            # Ricompensa
            reward = 100 if next_file == flag_file else -1

            # Aggiorna la Q-table
            Q[state, action] += alpha * (reward + gamma * np.max(Q[action]) - Q[state, action])

            # Passa allo stato successivo
            state = action

            # Incrementa il contatore delle iterazioni
            iterazioni += 1

    # Trova il percorso ottimale
    path = ['index.html']
    state = file_indices['index.html']

    while index_files[state] != flag_file:
        action = np.argmax(Q[state])
        path.append(index_files[action])
        state = action

    # restituisci path e numero di iterazioni
    return path, iterazioni 

def main():
    n_runs = 10
    times = []
    memory = []
    correct_flag_count = 0
    iterazioni_totali = 0  # Inizializza la variabile a zero

    for i in range(n_runs):
        # Percorso flag
        path, iterazioni = find_flag_path()

        # Misura il tempo di esecuzione
        start_time = timeit.default_timer()
        end_time = timeit.default_timer()
        time_elapsed = (end_time - start_time) * 1000  # converti il tempo in millisecondi
        times.append(time_elapsed)

        # Misura l'utilizzo della memoria
        mem_usage = memory_usage(find_flag_path, max_usage=True)
        memory.append(mem_usage)

        # Conta il numero di volte in cui l'algoritmo ha trovato la bandiera corretta
        if path[-1] == 'data.html':
            correct_flag_count += 1

        # Calcola il numero di iterazioni necessarie
        iterazioni_totali += iterazioni   

        print(i+1)
        print(f'Percorso per trovare la bandiera: {path}\n')
        print(f'Tempo di esecuzione: {time_elapsed:.10f} millisecondi')
        print(f'Utilizzo della memoria: {mem_usage:.2f} MB\n')

    # Calcola la percentuale di successo
    success_percentage = correct_flag_count / n_runs * 100

    # Calcola la media di tempo e memoria
    avg_time = sum(times) / len(times)
    avg_mem = sum(memory) / len(memory)

    print(f'\nTempo medio di esecuzione: {avg_time:.10f} millisecondi')
    print(f'Utilizzo medio della memoria: {avg_mem:.2f} MB\n')
    print(f'Percentuale di successo: {success_percentage:.9f}%\n')
    print(f'Numero di iterazioni totali: {iterazioni_totali}\n')


    # Plot dei risultati
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].plot(range(n_runs), times)
    ax[0].set_xlabel('Numero di esecuzioni')
    ax[0].set_ylabel('Tempo di esecuzione (ms)')

    plt.subplots_adjust(wspace=0.5)

    ax[1].plot(range(n_runs), memory)
    ax[1].set_xlabel('Numero di esecuzioni')
    ax[1].set_ylabel('Utilizzo della memoria (MB)')
    plt.show()


if __name__ == '__main__':
    main()
