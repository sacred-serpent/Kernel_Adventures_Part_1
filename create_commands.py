def upload_file(src_path :str, dst_path :str, chunk_size :int=32):
    """Upload a binary file through stdin using multiple printf calls.
    @chunk_size: Amount of bytes to write per printf call
    """
    with open(src_path, 'rb') as f:
        src_bin = f.read()
    
    src_bin_chunks = [ src_bin[i:i+chunk_size] for i in range(0, len(src_bin), chunk_size) ]
    
    split_fmt_strings = [
        [r'\x' + hex( int(byte) )[2:].zfill(2) for byte in src_bin_chunks[i]]
        for i in range(len(src_bin_chunks))
    ]
    
    fmt_strings = [''.join(split_fmt_string) for split_fmt_string in split_fmt_strings]

    commands_str = ''
    commands_str += 'printf "{}" > {}\n'.format(fmt_strings[0], dst_path)
    for fmt_string in fmt_strings[1:]:
        commands_str += 'printf "{}" >> {}\n'.format(fmt_string, dst_path)
    
    return commands_str[:-1]


def enter(count :int):
    return '\n' * count


def create_commands_file(command_list :list, dst_path :str='commands.sh'):
    with open(dst_path, 'w') as f:
        for command_str in command_list:
            f.write(command_str + '\n')

# Put your commands here!

create_commands_file([
    enter(200),
    upload_file('su', '/home/user/su', 100),
    'ls -l /home/user/su',
    'chmod u+x /home/user/su',
    '/home/user/su',
    'echo $?'
])