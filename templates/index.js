<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Chat App</title>
    <script>
        async function sendMessage() {
            const message = document.getElementById('message').value;
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            const data = await response.json();
            document.getElementById('response').innerText = data.response;
        }
    </script>
</head>
<body>
    <h1>Flask Chat App with Bedrock</h1>
    <input type="text" id="message" placeholder="Type your message here">
    <button onclick="sendMessage()">Send</button>
    <p id="response"></p>
</body>
</html>
