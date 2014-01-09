#!/usr/bin/python

import sys
import getpass
import trello
import github
# locally
import setup


def get_issue_title_and_url(issue_number):
    '''
    connect to github
    get organisation
    get repo
    get issue
    get issue desc 
    get issue url
    '''

    pw = getpass.getpass(prompt='Enter your github password:')
    g = github.Github(setup.user, pw)

    print 'Getting issue details from github ...'
    org = g.get_organization(setup.organization)
    repo = org.get_repo('viamirror-ios-osx')
    issue = repo.get_issue(issue_number)
    return issue.title, issue.html_url


def get_token_url():
    conn = trello.TrelloApi(setup.app_key)
    print conn.get_token_url('Issue2Trello', expires='30days', write_access=True)

def add_issue_to_trello(issue_number, issue_title, issue_url):
    '''
    connect to trello
    set token
    get board
    get list
    create card on list with name and description
    '''

    print 'Creating new card for issue on Trello ...'
    conn = trello.TrelloApi(setup.app_key)
    conn.set_token(setup.token)
    card_title = 'Issue %d: %s' % (issue_number, issue_title)
    new_card_id = conn.lists.new_card(setup.list_id, card_title)['id']
    conn.cards.update_desc(new_card_id, issue_url)
    conn.cards.new_label(new_card_id, 'red')

def main(issue_number):
    issue_title, issue_url = get_issue_title_and_url(issue_number)
    add_issue_to_trello(issue_number, issue_title, issue_url)

if __name__=="__main__":

    if len(sys.argv) < 2:
        print 'Usage: %s <issue_number>' % sys.argv[0]
        exit(1)
    issue = int(sys.argv[1])

    main(issue)
