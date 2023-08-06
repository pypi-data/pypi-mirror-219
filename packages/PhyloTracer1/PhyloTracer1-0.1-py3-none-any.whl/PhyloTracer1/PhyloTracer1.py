import argparse

# 创建解析器
parser = argparse.ArgumentParser(description='Process some integers.')

# 添加参数
parser.add_argument('--Gene_tree', type=str, help='Path to the Gene_tree file')
parser.add_argument('--Gene_len', type=str, help='Path to the Gene_len file')

# 解析参数
args = parser.parse_args()

# 现在你可以使用 args.Gene_tree 和 args.Gene_len 来访问用户提供的值
print('Gene_tree:', args.Gene_tree)
print('Gene_len:', args.Gene_len)

def main():
    # Argument parsing, main logic, etc. goes here

if __name__ == "__main__":
    main()
