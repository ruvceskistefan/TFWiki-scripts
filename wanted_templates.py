from utils import plural, time_and_date, whatlinkshere
from wikitools import wiki
from wikitools.page import Page

verbose = False

def main(w):
  wanted_templates = []
  for template in w.get_all_wanted_templates():
    use_count = Page(w, template).get_transclusion_count()
    if use_count > 0:
      if verbose:
        print(f'Template {template} has {use_count} uses')
      wanted_templates.append([use_count, template])

  output = """\
{{{{DISPLAYTITLE: {count} wanted templates}}}}
List of all <onlyinclude>{count}</onlyinclude> broken template transclusions (usually due to typos or missing dictionary entries). Data as of {date}.

== List ==\n""".format(
    count=sum(i[0] for i in wanted_templates),
    date=time_and_date())

  for count, title in sorted(wanted_templates, reverse=True):
    output += f'* [{whatlinkshere(title, count)} {title} has {plural.uses(count)}]\n'
  return output

if __name__ == '__main__':
  verbose = True
  w = wiki.Wiki('https://wiki.teamfortress.com/w/api.php')
  with open('wiki_wanted_templates.txt', 'w') as f:
    f.write(main(w))
  print(f'Article written to {f.name}')
