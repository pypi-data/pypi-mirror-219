# Emoticon cz

Plugin de [commitizen](https://commitizen-tools.github.io/commitizen/) el cual ya incorpora emojis en los tipos de cambios que realizamos, ademas de que parsea los codigos de JIRA y los issues.

## Instalacion

```python
pip install cz_emoticon
```

## Configuracion

Dentro del archivo de configuracion del cz que se encuentra en la raiz de tu proyecto puedes agregar las siguientes configuraciones

```yaml

bump_message = "🔖 release[$new_version]: $current_version → $new_version"
jira_prefix = "JIRA"
jira_url = "https://ayigroup.atlassian.net"
git_repo = ""
project_name = "Data Lake"
support_email = "support@ayi.group"

```

bump_message: es obligatorio que este parametro este configurado tal cual como se muestra en este readme

jira_prefix: es el codigo jira del proyecto el cual es necesario para identificarlo dentro del mensaje. Por ejemplo: PR es el identificador del proyecto al colocar dentro de nuestro footer PR-54 junto con el parametro jira_url generara la url de dicho issue.

jira_url: es la url base de nuestro jira y es necesario junto con jira_prefix para poder generar las url de los issues de forma automatica

git_repo: es el repositorio de nuetro gitlab o github, permite generar la url de forma automatica asi los issues de esas plataformas, colocando la url el plugin identificara si es de gitlab o github. Por ejemplo: si colocamos en nuestro footer #34 el plugin automaticamente generara la url del issue #34 usando como base la url que colocamos en git_repo.

project_name: es el nombre de nuestro proyecto, este estara disponible en el changeloge

support_email: el email de contacto de soporte de nuestra app, para que pueda ser visualizado en el changelog.

## Ejemplos

```
git cz

Seleccione el tipo de cambio que va a realizar: 
📝 docs: Cuando solo se modifica documentacion.

🚩 Cual es el alcance de este cambio? (nombre de clase o archivo): (es obligatorio colocar un scope):
init

✏️ Escriba un resumen breve e imperativo de los cambios en el codigo: (minusculas y sin punto):
Documentacion inicial del proyecto

📄 Proporcione informacion contextual adicional sobre los cambios de codigo: (pulse [intro] para omitir):
Se genero la documentacion inicial del proyecto con los standares a usar

🚨 Se trata de un CAMBIO IMPORTANTE? Relacionado con MAJOR en SemVer:
N

💬 Pie de pagina. Informacion sobre cambios de ultima hora y problemas de referencia que cierra esta confirmación: (pulse [enter] para saltar):
Ref: PR-123 #43

El commit generado sería:
📝 docs[init]: Documentacion inicial del proyecto (Ref: PR-123 #43)
```
En el ejemplo agregamos tanto el codigo jira como el issue de nuestro git para que el plugin genere automaticamente las urls correspondientes.


## Autor

Javier Baigorria (jdbaigorria@gmail.com)
