To run the chat application, you can run either IPv4 or IPv6 version
Paste these into command line to run the file client.py
python client.py

Then you type in either 4 or 6 for your IP version. The chat app will start

Chat actions:
Send '/all <message>' command to send a message to all clients.
Send '/pm <client name> <message>' command to send a private message to a client      
Send '/file <client name> <file path>' command to send a file to a client
Send '/receive <file path> as <file name>' command to receive the file from the server
Send '/see' to see all registered clients, online clients and available groups        
Send '/status <client name>' to check current status of a client
Send '/command' to see instructions on how to use the chat application
Send '/create <group name>' to create a new group. Group name should only be 1 word
Send '/rename <group name> <new group name>' to rename group. Group name should only be 1 word. Only for group creator
Send '/add <member> <member>...<member>' to add members to a group. Only for group creator
Send '/remove <member> <member>...<member>' to remove members from a group. Only for group creator
Send '/delete <group name>' to delete your created group. Only for group creator
Send '/members <group name>' to see members of the group
Send '/join <group name>' to join an existing group
Send '/leave <group name>' to leave your joined group
Send '/send <group name> <message>' to send a message to your joined group
Type '/quit' to go offline
