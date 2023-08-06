from abiparser import ContractABI

abi = ContractABI('tests/uniswap.sol/IUniswapV2Router.json')

assert abi.name == 'IUniswapV2Router'
assert abi.file_path == 'tests/uniswap.sol/IUniswapV2Router.json'
assert abi.constructor is None
assert abi.fallback is None
assert abi.receive is None
assert abi.get_function_by_name('swapExactTokensForTokens') is not None
