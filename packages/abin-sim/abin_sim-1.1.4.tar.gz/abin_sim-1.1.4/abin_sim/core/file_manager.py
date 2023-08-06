from pathlib3x import Path


def make_return(env: str, secret: dict, filepath: str, file: str) -> dict:
    try:
        # path = Path(filepath) / app
        envjs = False
        conffiles = False
        path = Path(filepath)
        # path.rmtree(ignore_errors=True)
        # path.mkdir()
        if file == 'env':
            arqenv = open(f'{path}/.env', 'w')
            conffiles = True
        elif file == 'env.js' and env == 'local':
            envjs = True
            arqenv = open(f'{path}/src/assets/env.js', 'w')
        else:
            arqenv = open(f'{path}/{file}', 'w')
            conffiles = True
    except Exception as e:
        retorno = {'Status': False, 'Message': e, 'EnvJS': envjs, 'ConfFiles': conffiles}
    else:
        if file == 'env':
            for k, v in secret.items():
                arqenv.write(f'{k}={v}' + '\n')
        else: 
            arqenv.write(secret)
        arqenv.close()
        if envjs:
            retorno = {'Status': True, 'Message': '', 'EnvJS': envjs, 'ConfFiles': conffiles}
        else:
            retorno = {'Status': True, 'Message': '', 'EnvJS': envjs, 'ConfFiles': conffiles}
    return retorno
