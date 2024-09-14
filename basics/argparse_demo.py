import matplotlib.pyplot as plt
import pandas as pd
import argparse as ap

if __name__ == '__main__':
    parser = ap.ArgumentParser(description='CS439: Simple Scatter Plot Example')
    parser.add_argument('-i', '--input', type=str, required=True, help='Path of Excel workbook')
    parser.add_argument('-x', type=str, default='Acceleration', help='Column to map to x axis')
    parser.add_argument('-y', type=str, default='Range', help='Column to map to y axis')
    parser.add_argument('-c', '--color', type=str, default='Price', help='Column to map to color')
    parser.add_argument('-s', '--size', type=float, default='100', help='Point size')
    args = parser.parse_args()

    df = pd.read_excel(args.input)

    fig, ax = plt.subplots(1,1, figsize=(12,8))
    
    fig.suptitle(f'{args.y} vs {args.x} (color={args.color})', weight='bold', fontsize='x-large')

    scat = ax.scatter(df[args.x], df[args.y], c=df[args.color], edgecolor=[0.,0.,0.], alpha=0.5, s=args.size)
    fig.colorbar(scat, ax=ax, label=args.color)
    ax.set_xlabel(args.x, weight='bold')
    ax.set_ylabel(args.y, weight='bold')

    plt.show()