# -*- coding: utf-8 -*-
import json
import sys
import settings
from jinja2 import Environment, FileSystemLoader
from os.path import join, exists
from os import makedirs, listdir
from shutil import copytree, rmtree
import mimetypes


def parse_json(path):
    f = open(path, 'r')
    return json.loads(f.read())


def main(argv):
    print "Parameters", argv
    env = Environment(loader=FileSystemLoader(settings.TEMPLATES))
    episodes = get_episodes()

    if len(argv) < 2:
        print "Not enough command line arguments"
        return

    print "Website located at", argv[1]
    website_path = argv[1]
    result_template_dir = join(website_path, "templates")
    if not exists(result_template_dir):
        makedirs(result_template_dir)
    create_overview(env, episodes, result_template_dir)
    for episode in episodes:
        create_episode(env, episode, result_template_dir)

    create_static_page(env, result_template_dir, 'about.html')
    if argv[0] == "init":
        # copy css javascript etc.
        result_static_dir = join(website_path, "static")
        if exists(result_static_dir):
            rmtree(result_static_dir)
        copytree(settings.STATIC, result_static_dir)

    elif argv[0] == "update":
        pass


def get_episodes():
    productions = listdir(settings.PRODUCTIONS)
    episodes = []

    for production in productions:
        if production.endswith(".json"):
            episodes.append(parse_json(join(settings.PRODUCTIONS, production)))
    return episodes


def get_audio_files(episode):
    files = []

    for service in episode['outgoing_services']:
        if service['uuid'] in settings.MEDIA_SERVER_UUIDS:
            for result in service['result_urls']:
                mime_type = list(mimetypes.guess_type(result))
                if mime_type[0] and mime_type[0].startswith('audio'):
                    if mime_type[0].endswith('ogg'):
                        mime_type[0] += '; codecs=vorbis'
                    files.append({'href': result, 'mime_type': mime_type[0]})
    return files


def get_chapters_json(episode):
    chapters = []
    for chapter in episode['chapters']:
        chapters.append({
            'start': chapter['start'],
            'title': chapter['title'],
            'href': chapter['url'],
        })
    return json.dumps(chapters)


def create_episode(env, episode, result_template_dir):
    audio_files = get_audio_files(episode)
    chapters = get_chapters_json(episode)
    template = env.get_template('episode.html')
    rendered = template.render(episode=episode, audio_files=audio_files,
                               chapters=chapters)

    # TODO: create better urls
    overview = open(join(result_template_dir, episode['uuid'] + '.html'), 'wb')
    overview.write(rendered.encode('utf-8'))
    overview.close()


def create_overview(env, episodes, result_template_dir):
    template = env.get_template('overview.html')
    rendered = template.render(episodes=episodes, title=settings.PODCAST_NAME)
    overview = open(join(result_template_dir, 'overview.html'), 'wb')
    overview.write(rendered.encode('utf-8'))
    overview.close()


def create_static_page(env, result_template_dir, html):
    template = env.get_template(html)
    rendered = template.render()
    overview = open(join(result_template_dir, html), 'wb')
    overview.write(rendered.encode('utf-8'))
    overview.close()

if __name__ == "__main__":
    print "Productions are at", settings.PRODUCTIONS

    # TODO: Parse this in the proper way, and validate arguments
    parameters = sys.argv[1:]
    main(parameters)
