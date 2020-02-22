from groupy.client import Client
from config import Config

# return the correct group based on Config value
def findGroup(client, groupName):
    for group in client.groups.list():
        if group.name.lower() == groupName.lower():
            return group

# Create a skeleton dictionary with members and keywords
def memberDictBuilder(members, keywords):
    memberDict = {}
    for member in members:
        memberDict.update({member[0] : {keyword: 0 for keyword in keywords}})

    return memberDict

# Populate dictionary values with accurate word counts
def getWordCounts(memberDict, messages, keywords):
    for message in messages:
        # If message is not plain text, ignore for now
        if not isinstance(message.text, str):
            continue
        for word in keywords:
            if word.lower() in message.text.lower():
                if message.user_id in memberDict.keys():
                    # add 1 to word count for specific user
                    memberDict[message.user_id][word] += 1
    return memberDict

# FIXME: as of right now, crudely displays data in command line
def displayData(finalDict, memberList, keywords):
    for user in finalDict.keys():
        for member in memberList:
            if user == member[0]:
                for keyword in keywords:
                    print(f'{member[1]} has mentioned "{keyword}" {finalDict[user][keyword]} times')

# Main function
def main():
    # Create groupy client from access token
    client = Client.from_token(Config.token)
    myGroup = findGroup(client, Config.groupName)
    # make sure group is newly refreshed
    myGroup.refresh_from_server()

    allMessages = list(myGroup.messages.list().autopage())

    memberList = []
    for member in myGroup.members:
        memberList.append((member.user_id, member.nickname))

    memberDict = memberDictBuilder(memberList, Config.keywords)

    countedMemberDict = getWordCounts(memberDict, allMessages, Config.keywords)

    displayData(countedMemberDict, memberList, Config.keywords)





if __name__ == "__main__":
    print('Starting Word Counter')
    main()
