import sys

def main():
    while True:
        command = input("> ").strip().replace(" ", "")
        if command == "quit":
            break
        
        command = f"0+{command}"
        command_segments = parse(command)
        print(run(command_segments))

    return 0

def parse(command: str):
    command_segments: list[str] = []
   
    # Parse additions first
    for segment in command.split(sep="+"):
        command_segments.append(segment)
        command_segments.append("+")

    _ = command_segments.pop()

    # Parse multiplication
    inserted: bool = False
    for index, segment in enumerate(command_segments):
        if inserted:
            inserted = False
            continue
        if not "*" in segment:
            continue
        negative_count = segment.count("-")
        segment = segment.replace("-", "")
        if negative_count % 2 == 1:
            command_segments.insert(index, "-")
            inserted = True
            index += 1
        command_segments[index] = segment

    # Parse negatives
    for index, segment in enumerate(command_segments):
        if not "-" in segment:
            continue
        if len(segment) == 1:
            continue
        segment = f"\n{segment}\n"
        segment = segment.split(sep="-")
        for i in range(len(segment)-1, 0, -1):
            segment.insert(i, "-")
        segment = [term for term in segment if term != "\n"]
        segment = list(map(lambda x: x.strip(), segment))
        buffer = command_segments[index+1:]
        command_segments = command_segments[:index]
        command_segments.extend(segment)
        command_segments.extend(buffer)
    
    return command_segments

def run(command_segments: list[str]):
    curr_number = int(command_segments.pop(0))
    direction: int = 1

    for command in command_segments:
        match command:
            case "+":
                pass
            case "-":
                direction *= -1
            case command if any([c for c in command if c == "*"]):
                command = command.split("*")
                curr_number += direction * int(command[0]) * int(command[1])
            case _:
                curr_number += direction * int(command)

    return curr_number

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)
