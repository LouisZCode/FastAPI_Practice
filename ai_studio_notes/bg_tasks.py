from datetime import datetime

def save_to_log(note_id : id, question : str, answer : str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open("ai_logs.txt", "a") as f:  # "a" = append, don't overwrite
        f.write(f"{timestamp} | Note {note_id} | Asked: {question} | Answer: {answer[:100]}...\n")