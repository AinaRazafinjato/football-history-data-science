def load_config(config_file):
    import json
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

def save_results(results, output_file):
    import json
    with open(output_file, 'w') as file:
        json.dump(results, file)

def log_message(message, log_file='app.log'):
    with open(log_file, 'a') as file:
        file.write(f"{message}\n")