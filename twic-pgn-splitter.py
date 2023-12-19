from argparse import ArgumentParser
from pathlib import Path
from typing import TextIO


def emit_single_game(f: TextIO) -> str:
    """Return single complete PGN from file."""
    pgn = []
    while True:
        # Header doesn't have a fixed size
        # Retrieving header line-by-line
        line = next(f)
        if line.startswith('['):
            pgn.append(line.strip())
            continue  # proceed getting the next line

        # Header finished

        # PGNs have empty line between header and SAN
        # that was already consumed by `next(fiter)`;
        # Next line in PGN contains game log in SAN
        # (Standard/Short Algebraic Notation)

        # For PGNs that have SAN separated over several lines
        # (Caissa, Mega), run an inside loop that collects this SAN log
        san = ''
        while True:
            line = next(f).strip()
            if not line:
                # Consumed a line between SAN and next PGN header;
                # can return complete PGN
                break
            san += line + ' '

        pgn.append(san.strip())

        return pgn


def split_pgn(infile: Path):
    """Split PGN into internet and OTB games."""
    root = infile.expanduser().parent

    internet = []
    otb = []

    sites = {
        '[Site "chess.com INT"]',
        '[Site "chess24.com INT"]',
        '[Site "lichess.org INT"]',
        '[Site "AuNix INT"]',
        '[Site "Chess Supersite INT"]',
        '[Site "Europe-Chess INT"]',
        '[Site "Europe-Echecs INT"]',
        '[Site "ICC INT"]',
        '[Site "ICCF INT"]',
        '[Site "PlayChess INT"]',
        '[Site "Playchess.com INT"]',
        '[Site "Premium Chess Arena INT"]',
        '[Site "Tornelo INT"]',
        '[Site "chessdom.com INT"]',
        '[Site "playchess.com INT"]',
    }

    with open(infile, encoding='latin-1') as f:
        while True:
            try:
                pgn = '\n'.join(emit_single_game(f))
                if any(s.lower() in pgn.lower() for s in sites):
                    internet.append(pgn)
                else:
                    otb.append(pgn)
            except StopIteration:
                # EOF
                break
    
    with open(root / 'internet.pgn', 'w') as f:
        f.write('\n\n'.join(internet))
    
    with open(root / 'otb.pgn', 'w') as f:
        f.write('\n\n'.join(otb))



def main():
    ap = ArgumentParser()
    ap.add_argument('infile', type=Path, help='Input file (PGN)')

    args = ap.parse_args()

    split_pgn(args.infile)


if __name__ == '__main__':
    main()