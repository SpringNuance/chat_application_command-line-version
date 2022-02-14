from datetime import datetime

def broadcast(message, onlineClients):
    for name in onlineClients:
        onlineClients[name].send(bytes(message, "utf8"))

def privateMessage(senderName, message, onlineClients, registeredClients, lastOnline, bufferedMessages): 
    receiverName = message.split()[0]
    if receiverName not in registeredClients:
        onlineClients[senderName].send(bytes("There is no users of that name in the server. Please check if there are misspellings", "utf8"))
    elif receiverName not in onlineClients:
        onlineClients[senderName].send(bytes(f"The user is currently offline. Last online {lastOnline[receiverName]}. \nThey will see your message when they come online again", "utf8"))
        timeStamp = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        messageBody = message.split(' ', 1)[1]
        bufferedMessages[receiverName].append("<" + timeStamp + "> " + senderName + ": " + messageBody)
    else: 
        timeStamp = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        messageBody = message.split(' ', 1)[1]
        onlineClients[receiverName].send(bytes("<" + timeStamp + "> " + senderName + ": " + messageBody, "utf8"))
        onlineClients[senderName].send(bytes(f"{receiverName} has seen your message", "utf8"))

def sendFile(senderName, message, onlineClients, fileDatabase):
    receiverName = message.split()[0]
    filePath = message.split()[1]
    fileOpen = open(filePath)
    fileData = fileOpen.read()
    onlineClients[receiverName].send(bytes(f"A file is sent to you by user {senderName}. Would you like to save the file?\nType '/receive {filePath} as <your chosen file name>' to receive the file\n>>>", "utf8"))
    fileDatabase[filePath] = fileData

def receiveFile(senderName, message, onlineClients, fileDatabase):
    filePath = message.split()[0]
    fileName = message.split()[2]
    if filePath not in fileDatabase:
        onlineClients[senderName].send(bytes(f"There is no file {filePath} in the server. Please check misspellings", "utf8"))
    else:
        fileData = fileDatabase[filePath]
        onlineClients[senderName].send(bytes(f"The file has been successfully saved\n{fileData}\n{fileName}", "utf8"))

def seeAll(senderName, onlineClients, registeredClients, groupCreator):
    registeredClientsInfo = "Registered clients: "
    for name in registeredClients:
        registeredClientsInfo += name + ", "
    registeredClientsInfo = registeredClientsInfo[:-2]

    onlineClientsInfo = "Online clients: "
    for name in onlineClients:
        onlineClientsInfo += name + ", "
    onlineClientsInfo = onlineClientsInfo[:-2]

    groupsInfo = ""
    if (len(groupCreator) == 0):
        groupsInfo = "No available groups  "
    else:
        groupsInfo = "Available groups: "
        for groupName in groupCreator:
            groupsInfo += groupName + ", "
    groupsInfo = groupsInfo[:-2]
    
    onlineClients[senderName].send(bytes(f"{registeredClientsInfo}\n{onlineClientsInfo}\n{groupsInfo}\n", "utf8"))

def clientStatus(senderName, message, onlineClients, registeredClients, lastOnline):
    receiverName = message
    if receiverName not in registeredClients:
        onlineClients[senderName].send(bytes(f"There is no such user {receiverName} in the server", "utf8"))
    if receiverName in onlineClients:
        onlineClients[senderName].send(bytes(f"The user {receiverName} is currently online", "utf8"))
    else: 
        onlineClients[senderName].send(bytes(f"The user {receiverName} is currently offline. Last online {lastOnline[receiverName]}", "utf8"))
    
def instructions(senderName, onlineClients):
    # Universal broadcast message 
    # Command /all <message>
    onlineClients[senderName].send(bytes("\nSend '/all <message>' command to send a message to all clients.", "utf8"))
    
    # Private message chat
    # Command /pm <client name> <message>
    onlineClients[senderName].send(bytes("\nSend '/pm <client name> <message>' command to send a private message to a client", "utf8"))
    
    # File transfer
    # Command /file <client name> <file path>
    onlineClients[senderName].send(bytes("\nSend '/file <client name> <file path>' command to send a file to a client", "utf8"))
    # Command /receive <file path> as <file name>
    onlineClients[senderName].send(bytes("\nSend '/receive <file path> as <file name>' command to receive the file from the server", "utf8"))
    
    # Server stats
    # Command /see
    onlineClients[senderName].send(bytes("\nSend '/see' to see all online clients and available groups", "utf8"))
    # Command /status <client name>
    onlineClients[senderName].send(bytes("\nSend '/status <client name>' to check current status of a client", "utf8"))
    # Command /command 
    onlineClients[senderName].send(bytes("\nSend '/command' to see instructions on how to use the chat application", "utf8"))

    # Group chat
    # Command /create <group name>
    onlineClients[senderName].send(bytes("\nSend '/create <group name>' to create a new group. Group name should only be 1 word", "utf8"))
    # Command /rename <group name> <new group name>. Only for group creator
    onlineClients[senderName].send(bytes("\nSend '/rename <group name> <new group name>' to rename group. Group name should only be 1 word. Only for group creator", "utf8"))
    # Command /add <group name> <member> <member>...<member>. Only for group creator
    onlineClients[senderName].send(bytes("\nSend '/add <member> <member>...<member>' to add members to a group. Only for group creator", "utf8"))
    # Command /remove <group name> <member> <member>...<member>. Only for group creator
    onlineClients[senderName].send(bytes("\nSend '/remove <member> <member>...<member>' to add members from a group", "utf8"))
    # Command /delete <group name>. Only for group creator
    onlineClients[senderName].send(bytes("\nSend '/delete <group name>' to delete your created group. Only for group creator", "utf8"))
    # Command /members <group name>
    onlineClients[senderName].send(bytes("\nSend '/members <group name>' to see members of the group", "utf8"))
    # Command /join <group name>. For any users
    onlineClients[senderName].send(bytes("\nSend '/join <group name>' to join an existing group", "utf8"))
    # Command /leave <group name>. For any users
    onlineClients[senderName].send(bytes("\nSend '/leave <group name>' to leave your joined group", "utf8"))
    # Command /send <group name> <message>. For any users
    onlineClients[senderName].send(bytes("\nSend '/send <group name> <message>' to send a message to your joined group", "utf8"))
    
    # Quitting chat
    # Command /quit
    onlineClients[senderName].send(bytes("\nType '/quit' to go offline", "utf8"))

def createGroup(senderName, message, groupCreator, groupMembers, onlineClients):
    groupName = message
    if groupName in groupCreator:
        onlineClients[senderName].send(bytes("The group " + groupName + " already exists. Please choose another name", "utf8"))
    else: 
        groupCreator[groupName] = senderName
        groupMembers[groupName] = [senderName]
        timeStamp = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        message = f"<{timeStamp}> {senderName} has created the group {groupName}"
        broadcast(message, onlineClients)
    
def renameGroup(senderName, message, groupCreator, groupMembers, onlineClients):
    oldGroupName = message.split()[0]
    newGroupName = message.split()[1]
    if oldGroupName not in groupCreator:
        onlineClients[senderName].send(bytes("The specified group does not exist. Please check misspellings", "utf8"))
    elif groupCreator[oldGroupName] != senderName:
        onlineClients[senderName].send(bytes("You do not have admin rights to rename the group. Only the creator can rename the group", "utf8"))
    else:
        groupCreator[newGroupName] = groupCreator.pop(oldGroupName)
        groupMembers[newGroupName] = groupMembers.pop(oldGroupName)
        timeStamp = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        message = f"<{timeStamp}> {senderName} has renamed the group {oldGroupName} as {newGroupName}"
        broadcast(message, onlineClients)

def addMembers(senderName, message, groupCreator, groupMembers, onlineClients, registeredClients):
    groupName = message.split()[0]
    addedMembers = message.split(' ', 1)[1].split()
    if groupName not in groupCreator:
        onlineClients[senderName].send(bytes("The specified group does not exist. Please check misspellings", "utf8"))
    elif senderName != groupCreator[groupName]:
        onlineClients[senderName].send(bytes("You do not have admin rights to add members to the group. Only the creator can add members to the group", "utf8"))
    else:
        for member in addedMembers:
            if member in registeredClients:
                groupMembers[groupName].append(member)
                onlineClients[senderName].send(bytes(f"User {member} has been added to your group {groupName}\n", "utf8"))
            else:
                onlineClients[senderName].send(bytes(f"User {member} does not exist in registered users and cannot be added to your group {groupName}\n", "utf8"))

def removeMembers(senderName, message, groupCreator, groupMembers, onlineClients):
    groupName = message.split()[0]
    removedMembers = message.split(' ', 1)[1].split()
    if groupName not in groupCreator:
        onlineClients[senderName].send(bytes("The specified group does not exist. Please check misspellings", "utf8"))
    elif senderName != groupCreator[groupName]:
        onlineClients[senderName].send(bytes("You do not have admin rights to remove members from the group. Only the creator can remove members from the group", "utf8"))
    else:
        for member in removedMembers:
            if member in groupMembers[groupName]:
                groupMembers[groupName].remove(member)
                onlineClients[senderName].send(bytes(f"User {member} has been removed from your group {groupName}\n", "utf8"))
            else:
                onlineClients[senderName].send(bytes(f"User {member} does not exist in the group {groupName} and cannot be removed from your group\n", "utf8"))

def deleteGroup(senderName, message, groupCreator, groupMembers, onlineClients):
    groupName = message
    if groupName not in groupCreator:
        onlineClients[senderName].send(bytes("The specified group does not exist. Please check misspellings", "utf8"))
    elif senderName != groupCreator[groupName]:
        onlineClients[senderName].send(bytes("You do not have admin rights to delete the group. Only the creator can delete the group", "utf8"))
    else:
        del groupCreator[groupName]
        del groupMembers[groupName]
        timeStamp = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        message = f"<{timeStamp}> {senderName} has deleted the group {groupName}"
        broadcast(message, onlineClients)

def seeMembers(senderName, message, groupCreator, groupMembers, onlineClients):
    groupName = message
    if groupName not in groupCreator:
        onlineClients[senderName].send(bytes("The specified group does not exist. Please check misspellings", "utf8"))
    else:
        admin = groupCreator[groupName]
        membersInfo = f"The member(s) in the group {groupName} are: "
        for member in groupMembers[groupName]:
            if member == admin: 
                membersInfo += f"{member}(admin), "
            else: 
                membersInfo += f"{member}, "
        membersInfo = membersInfo[:-2]
        onlineClients[senderName].send(bytes(membersInfo, "utf8"))

def joinGroup(senderName, message, groupCreator, groupMembers, onlineClients):
    groupName = message
    if groupName not in groupCreator:
        onlineClients[senderName].send(bytes("The specified group does not exist. Please check misspellings", "utf8"))
    elif senderName in groupMembers[groupName]:
        onlineClients[senderName].send(bytes(f"You have already joined the group {groupName}", "utf8"))
    else:
        groupMembers[groupName].append(senderName)
        timeStamp = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        message = f"<{timeStamp}> {senderName} has joined the group {groupName}"
        broadcast(message, onlineClients)

def leaveGroup(senderName, message, groupCreator, groupMembers, onlineClients):
    groupName = message
    if groupName not in groupCreator:
        onlineClients[senderName].send(bytes("The specified group does not exist. Please check misspellings", "utf8"))
    elif senderName == groupCreator[groupName]:
        onlineClients[senderName].send(bytes(f"You are admin of this group and thus cannot leave. Consider '/delete {groupName}' instead", "utf8"))
    elif senderName not in groupMembers[groupName]:
        onlineClients[senderName].send(bytes(f"You are not a member in the group {groupName}", "utf8"))
    else:
        groupMembers[groupName].remove(senderName)
        timeStamp = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        message = f"<{timeStamp}> {senderName} has left the group {groupName}"
        broadcast(message, onlineClients)
    
def sendGroupMessage(senderName, message, groupCreator, groupMembers, onlineClients, bufferedMessages):
    groupName = message.split()[0]
    groupMessage = message.split()[1]
    if groupName not in groupCreator:
        onlineClients[senderName].send(bytes("The specified group does not exist. Please check misspellings", "utf8"))
    elif senderName not in groupMembers[groupName]:
        onlineClients[senderName].send(bytes(f"You are not a member in the group {groupName} and thus cannot send a message. Consider '/join {groupName}' to join the group", "utf8"))
    else: 
        onlineMembersExceptSender = []
        offlineMembers = []
        for member in groupMembers[groupName]: 
            if member in onlineClients and member != senderName:
                onlineMembersExceptSender.append(member)
            else:
                offlineMembers.append(member)

        if len(groupMembers[groupName]) == 1:
            onlineClients[senderName].send(bytes(f"Your group has no members. Consider add more members with '/add {groupName} <member> <member>...'", "utf8"))
        else:
            timeStamp = datetime.now().strftime("%d/%m/%y %H:%M:%S")

            if len(onlineMembersExceptSender) == 0:
                onlineClients[senderName].send(bytes(f"All of the members are offline. They will see your message when they go online", "utf8"))
            else:
                seenMembers = "Members "
                for member in onlineMembersExceptSender:
                    seenMembers += f"{member}, "
                    onlineClients[member].send(bytes(f"<{timeStamp}> Group {groupName}, {senderName}: {groupMessage}", "utf8"))
                seenMembers = seenMembers[:-2] + " have seen your message"
                onlineClients[senderName].send(bytes(seenMembers, "utf8"))
            
            for member in offlineMembers:
                bufferedMessages[member].append(f"<{timeStamp}> Group {groupName}, {senderName}: {groupMessage}")

def quitOnline(senderName, onlineClients, lastOnline):
    del onlineClients[senderName]
    lastOnline[senderName] = datetime.now().strftime("%d/%m/%y %H:%M:%S")
    message = f"User {senderName} has quitted the chat"
    for name in onlineClients:
        onlineClients[name].send(bytes(message, "utf8"))