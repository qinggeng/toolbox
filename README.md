#Toolbox by chatgpt

所有代码基本都是由chatgpt生成, 我只是gpt的传声筒

## poetry的问题

### poetry add 失败

运行如下指令即可：
```bash
PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring poetry add <package-name>
```