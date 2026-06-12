#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path
from textwrap import indent

PACKS_DIR = Path(__file__).resolve().parent.parent / 'packs'


def pack_names():
    names = sorted([p.stem for p in PACKS_DIR.glob('*.json')])
    return names


def load_pack(name):
    path = PACKS_DIR / f'{name}.json'
    if not path.exists():
        raise FileNotFoundError(f'Pack not found: {path}')
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def list_packs():
    print('Available packs:')
    for item in pack_names():
        print(f' - {item}')


def display_pack(name, index):
    pack = load_pack(name)
    prompts = pack.get('prompts', [])
    if index >= len(prompts):
        raise IndexError(f'No prompt index {index} for pack {name}')
    prompt = prompts[index]
    print(f"Pack: {name} | Prompt {index + 1}/{len(prompts)}")
    print('Prompt:')
    print(indent(prompt.get('prompt', ''), '  '))
    if 'notes' in prompt:
        print('Notes:')
        print(indent(prompt['notes'], '  '))


def usage():
    print('Usage:')
    print('  prompt_pack_runner.py list')
    print('  prompt_pack_runner.py show <pack> <index>')
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        usage()
    command = sys.argv[1].lower()
    if command == 'list':
        list_packs()
    elif command == 'show':
        if len(sys.argv) != 4:
            usage()
        name = sys.argv[2]
        index = int(sys.argv[3])
        display_pack(name, index)
    else:
        usage()


if __name__ == '__main__':
    main()
