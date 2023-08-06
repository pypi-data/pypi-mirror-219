from collections import OrderedDict
import os, re
from commitizen import git, config
from commitizen.config.base_config import BaseConfig
from commitizen.cz.base import BaseCommitizen
from commitizen.defaults import MINOR, PATCH, MAJOR
from commitizen.cz.utils import multiple_line_breaker, required_validator
from commitizen.exceptions import CommitizenException, ExitCode


class MissingCzExtraParamsConfigError(CommitizenException):
    exit_code = ExitCode.MISSING_CZ_CUSTOMIZE_CONFIG
    message = "fatal: los parametros extras no estan definidos en el archivo de configuracion."

def parse_scope(text):
    if isinstance(text, str):
        text = text.strip(".").strip()

    return required_validator(text, msg="El scope es requerido.")

def parse_subject(text):
    if isinstance(text, str):
        text = text.strip(".").strip()

    return required_validator(text, msg="El asunto de cambio es requerido.")

def parse_url(commit_message):
    url_pattern = re.compile(r"(?i)\b((?:https?://)?(?:www\.)?\w+\.\w+\.\w+(?:/\S*)?)\b")

    def replace_url(match):
        url = match.group(0)
        if url.startswith(("http://", "https://")):
            return f"[*link*]({url})"
        else:
            return f"[*link*](https://{url})"

    paresed_commit_message = re.sub(url_pattern, replace_url, commit_message)

    return paresed_commit_message

def parse_emails(commit_message):
    # Expresión regular para encontrar direcciones de correo electrónico
    email_pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")

    def replace_email(match):
        email = match.group(0)
        username = email.split("@")[0]
        return f"[*{username}*]({email})"

    # Reemplazar las direcciones de correo electrónico en el texto original utilizando una función de reemplazo personalizada
    paresed_commit_message = re.sub(email_pattern, replace_email, commit_message)

    return paresed_commit_message

def parse_issues(commit_message: str, remote: str):
# Expresión regular para encontrar el patrón '#<números>'
    pattern = r'#(\d+)'
    suffix: str = ""
    # Obtengo el sufijo para poder armar la url de issue
    if 'github' in remote:
        suffix = "/issues/"
    if 'gitlab' in remote:
        suffix = "/-/issues/"
    # Función de reemplazo que genera la URL del issue
    def replace_issue(match):
        issue_number = match.group(1)
        return f'[#{issue_number}]({remote}{suffix}{issue_number})'  # Reemplaza con la URL de tu repositorio y el sufijo que corresponde
    # Reemplazar el patrón en el footer utilizando la función de reemplazo
    paresed_commit_message = re.sub(pattern, replace_issue, commit_message)
    return paresed_commit_message

def parse_jira_codes(commit_message, jira_base_url, jira_code):
    jira_pattern = fr"(\b({jira_code}-[0-9]+)\b)"
        
    def replace_issue(match):
        jira_code = match.group(1)
        return fr'[{jira_code}]({jira_base_url}/browse/{jira_code})'  # Reemplaza con la URL de jira
    # Reemplazar el patrón en el footer utilizando la función de reemplazo
    paresed_commit_message = re.sub(jira_pattern, replace_issue, commit_message)
    return paresed_commit_message
    
class EmoticonCz(BaseCommitizen):

    bump_message = "🔖 release[$new_version]: $current_version → $new_version"
    bump_pattern = r"^(((🚨 BREAKING CHANGE|✨ feat|🐛 fix|♻️ refactor|⚡ perf)(\[.+\])(!)?)):"
    bump_map = OrderedDict(
        (
            (r"^.+!$", MAJOR),
            (r"^✨ feat", MINOR),
            (r"^🐛 fix", PATCH),
            (r"^♻️ refactor", PATCH),
            (r"^⚡ perf", PATCH),
        )
    )
    bump_map_major_version_zero = OrderedDict(
        (
            (r"^.+!$", MINOR),
            (r"^✨ feat", MINOR),
            (r"^🐛 fix", PATCH),
            (r"^♻️ refactor", PATCH),
            (r"^⚡ perf", PATCH),
        )
    )
    commit_parser = r"(?P<change_type>✨ feat|🐛 fix|📝 docs|🎨 style|♻️ refactor|⚡ perf|🧪 test|📦 build|🚀 ci|🔧 chore|⏪ revert)(?:\[(?P<scope>[^()\s]*)\])(?P<breaking>!)?(?P<message>[^()\r\n]*)(?:\((?P<footer>.*)\))?"
    change_type_map = {
        "✨ feat": "✨ Feat",
        "🐛 fix": "🐛 Fix",
        "♻️ refactor": "♻️ Refactor",
        "⚡ perf": "⚡ Perf",
        "📝 docs": "📝 Docs",
        "🎨 style": "🎨 Style",
        "🧪 test": "🧪 Test",
        "📦 build": "📦 Build",
        "🚀 ci": "🚀 CI",
        "🔧 chore": "🔧 Chore",
        "⏪ revert": "⏪ Revert",
    }
    changelog_pattern = r"^(🚨 BREAKING CHANGE|✨ feat|🐛 fix|📝 docs|🎨 style|♻️ refactor|⚡ perf|🧪 test|📦 build|🚀 ci|🔧 chore|⏪ revert)(.*)?(!)?:"


    conf = config.read_cfg()
    jira_prefix = ""
    jira_url = ""
    git_repo = ""
    project_name = ""
    support_email = ""
    if "jira_prefix" in conf.settings:
        jira_prefix = conf.settings["jira_prefix"]
    if "jira_url" in conf.settings:
        jira_url = conf.settings["jira_url"]
    if "git_repo" in conf.settings:
        git_repo = conf.settings["git_repo"]
    if "project_name" in conf.settings:
        project_name = conf.settings["project_name"]
    if "support_email" in conf.settings:
        support_email = conf.settings["support_email"]


    def questions(self) -> list:
        return [
            {
                "type": "list",
                "name": "prefix",
                "message": "Seleccione el tipo de cambio que va a realizar",
                "choices": [
                    {
                        "value": "🐛 fix",
                        "name": "🐛 fix: Cuando se arregla un error. Relacionado con PATCH en SemVer.",
                        "key": "x",
                    },
                    {
                        "value": "✨ feat",
                        "name": "✨ feat: Cuando se añade una nueva funcionalidad. Relacionado con MINOR en SemVer.",
                        "key": "f",
                    },
                    {
                        "value": "📝 docs",
                        "name": "📝 docs: Cuando solo se modifica documentacion.",
                        "key": "d",
                    },
                    {
                        "value": "🎨 style",
                        "name": (
                            "🎨 style: Cambios de legibilidad o formateo de codigo que no afecta a funcionalidad. (white-space, formatting, missing semi-colons, etc)."
                        ),
                        "key": "s",
                    },
                    {
                        "value": "♻️ refactor",
                        "name": (
                            "♻️ refactor: Cambio de codigo que no corrige errores ni añade funcionalidad, pero mejora el codigo."
                        ),
                        "key": "r",
                    },
                    {
                        "value": "⚡ perf",
                        "name": "⚡ perf: Usado para mejoras de rendimiento.",
                        "key": "p",
                    },
                    {
                        "value": "🧪 test",
                        "name": (
                            "🧪 test: Si añadimos o arreglamos tests existentes."
                        ),
                        "key": "t",
                    },
                    {
                        "value": "📦 build",
                        "name": (
                            "📦 build: Cuando el cambio afecta al compilado del proyecto o dependencias externas (ejemplo: pip, docker, npm)."
                        ),
                        "key": "b",
                    },
                    {
                        "value": "🚀 ci",
                        "name": (
                            "🚀 ci: el cambio afecta a ficheros de configuracion y scripts relacionados con la integracion continua (ejemplo: .gitlabc-ci.yaml)."
                        ),
                        "key": "c",
                    },
                    {
                        "value": "🔧 chore",
                        "name": (
                            "🔧 chore: tareas rutinarias que no sean especificas de una feature o un error (ejemplo: add .gitignore, instalar una dependencia, primer commit)."
                        ),
                        "key": "h",
                    },
                    {
                        "value": "⏪ revert",
                        "name": (
                            "⏪ revert: si el commit revierte un commit anterior. Deberia indicarse el hash del commit que se revierte."
                        ),
                        "key": "z",
                    },
                ],
            },
            {
                "type": "input",
                "name": "scope",
                "message": (
                    "🚩 Cual es el alcance de este cambio? (nombre de clase o archivo): (es obligatorio colocar un scope)\n"
                ),
                "filter": parse_scope,
            },
            {
                "type": "input",
                "name": "subject",
                "filter": parse_subject,
                "message": (
                    "✏️ Escriba un resumen breve e imperativo de los cambios en el codigo: (minusculas y sin punto)\n"
                ),
            },
            {
                "type": "input",
                "name": "body",
                "message": (
                    "📄 Proporcione informacion contextual adicional sobre los cambios de codigo: (pulse [intro] para omitir)\n"
                ),
                "filter": multiple_line_breaker,
            },
            {
                "type": "confirm",
                "message": "🚨 Se trata de un CAMBIO IMPORTANTE? Relacionado con MAJOR en SemVer",
                "name": "is_breaking_change",
                "default": False,
            },
            {
                "type": "input",
                "name": "footer",
                "message": (
                    "💬 Pie de pagina. Informacion sobre cambios de ultima hora y problemas de referencia que cierra esta confirmación: (pulse [enter] para saltar)\n"
                ),
            },
        ]

    def message(self, answers: dict) -> str:
        prefix = answers["prefix"]
        scope = answers["scope"]
        subject = answers["subject"]
        body = answers["body"]
        footer = answers["footer"]
        is_breaking_change = answers["is_breaking_change"]
        breaking = ""

        if scope:
            scope = f"[{scope}]"
        if body:
            body = f"\n\n{body}"
        if is_breaking_change:
            footer = f"BREAKING CHANGE: {footer}"
            breaking = "!"
        if footer:
            footer = f"\n\n({footer})"

        message = f"{prefix}{scope}{breaking}: {subject}{body}{footer}"

        return message

    def example(self) -> str:
        return (
            "fix[main.py]: correct minor typos in code\n"
            "\n"
            "see the issue for details on the typos fixed\n"
            "\n"
            "(closes issue #12)"
        )

    def schema(self) -> str:
        return (
            "<type>[<scope>]: <subject>\n"
            "<BLANK LINE>\n"
            "<message>\n"
            "<BLANK LINE>\n"
            "(BREAKING CHANGE: <footer>)"
        )

    def schema_pattern(self) -> str:
        return r"(✨ feat|🐛 fix|📝 docs|🎨 style|♻️ refactor|⚡ perf|🧪 test|📦 build|🚀 ci|🔧 chore|⏪ revert|🔖 release)(\[[^()\s]{3,}\])(!)?:\s([^()\s]*)(\((.*)\))?"

    def info(self) -> str:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(dir_path, "conventional_commits_info.txt")
        with open(filepath, "r") as f:
            content = f.read()
        return content
    
    def changelog_message_builder_hook(
        self, parsed_message: dict, commit: git.GitCommit
    ) -> dict:
        

        parsed_message['hash'] = commit.rev
        parsed_message['short_hash'] = commit.rev[0:8]
        parsed_message['author'] = commit.author
        parsed_message['email'] = commit.author_email
        parsed_message['developer'] = f"[{commit.author}]({commit.author_email})"
        parsed_message["footer"] = parse_emails(parse_url(self.__extract_footer(commit)))

        if self.project_name:
            parsed_message["project_name"] = self.project_name

        if self.support_email:
            parsed_message["support_email"] = self.support_email

        if self.jira_prefix and self.jira_url:
            parsed_message["footer"] = parse_jira_codes(parsed_message["footer"], self.jira_url, self.jira_prefix)

        if self.git_repo:
            parsed_message["footer"] = parse_issues(parsed_message["footer"], self.git_repo)

        f = open ('/home/javier/projects/emoticon/holamundo.txt','a')
        f.write(parsed_message.__repr__() + "\n")
        f.close()

        return parsed_message
    
    def __extract_footer(self, commit: git.GitCommit):
        footer_pattern = r"\((.*?)\)"
        matches = re.findall(footer_pattern, commit.body)
        return ", ".join(matches) 
    
    def __extract_body(self, commit: git.GitCommit):
        footer_pattern = r"\((.*?)\)"
        parts = re.split(footer_pattern, commit.body)
        body = parts[0].strip() if parts else commit.body.strip()
        return body
