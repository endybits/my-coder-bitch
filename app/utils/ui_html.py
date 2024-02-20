def htmlUI():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- <link rel="stylesheet" href="style.css"> -->
    <title>AI-driven Cloud Assistant</title>
    <style>
        body, html {
            font-family: 'Arial', sans-serif;
            height: 100%;
            width: 100%;
            margin: 0;
            display: flex;
            justify-content: center;
        }

        /* min-h-screen bg-white text-black flex flex-col */
        .chat-ai-section {
            min-height: 90vh;
            background-color: #FFF;
            color: #000;
            display: flex;
            flex-direction: column;
            width: 100%;
            max-width: 800px;
            border-radius: 6px;
            border: 1px solid #eaeaea
        }

        /* flex items-center justify-center h-16 border-b */
        .chat-session-header {
            background-color: #FFF;
            height: 4rem;
            border-bottom: 1px solid #eaeaea;
            border-top: 1px solid #eaeaea;    
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* text-2xl font-bold */
        .chat-session-header h1 {
            font-size: 1.5rem;
            font-weight:700;
            padding-left:.5rem;
        }

        /* flex-1 overflow-auto p-4 */
        .chat-session-main {
            flex: 1;
            overflow: auto;
            padding: 1.5rem;
        }

        /* flex flex-col gap-4 */
        .chat-container {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        /* flex flex-col gap-4 */
        .chat-bubble {
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        /* p-2 rounded-lg */
        .chat-bubble-ai .chat-bubble-user {
            padding: 1rem;
            border-radius: 6px;
        }

        .font-semibold {
            font-weight: 600;
            padding: 0%;
            margin-top: 0;
            margin-bottom: 4px;
        }

        .text-sm {
            font-size: 0.875rem;
            margin-top: 0;
            margin-bottom: 0;
        }


        /* h-20 border-t p-4 */
        .chat-session-footer {
            background-color: #FFF;
            height: 4rem;
            border-top: 1px solid #eaeaea;
            padding: 1.5rem;
        }

        /* flex items-center gap-2 */
        .chat-input {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        /* flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 flex-1 */
        .chat-input-textarea {
            display: flex;
            height: 3rem;
            width: 100%;
            resize: none;
            border-radius: 6px;
            border: 1px solid #e2e8f0;
            background-color: #f7fafc;
            padding: 0.75rem;
            font-size: 0.875rem;    
        }

        /* inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2 */
        .chat-input button {
            display: inline-flex;
            align-items: center;
            /* justify-content: center; */
            /* white-space: nowrap; */
            border-radius: 6px;
            font-size: 0.875rem;
            font-weight: 600;
            /* transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out; */
            outline: none;
            background-color: #000;
            color: #fff;
            cursor: pointer;
            padding: 0.75rem 1.5rem;
        }
    </style>
</head>
<body>
    <div class="chat-ai-section">
        <header class="chat-session-header">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="h-6 w-6 mr-2"
            >
                <path d="M12 8V4H8"></path>
                <rect width="16" height="12" x="4" y="8" rx="2"></rect>
                <path d="M2 14h2"></path>
                <path d="M20 14h2"></path>
                <path d="M15 13v2"></path>
                <path d="M9 13v2"></path>
            </svg>
            <h1 class="text-2xl font-bold">AI Assistant</h1>
        </header>
        <main class="chat-session-main">
            <div class="chat-container">
                
                <!-- AI and User Bubble examples 
                <div class="chat-bubble">
                    <div class="chat-bubble-ai">
                        <p class="font-semibold">AI Assistant:</p>
                        <p class="text-sm">Hello! How can I assist you today?</p>
                    </div>
                </div>
                
                <div class="chat-bubble">
                    <div class="chat-bubble-user">
                        <p class="font-semibold">User:</p>
                        <p class="text-sm">What's the weather like today?</p>
                    </div>
                </div>
                -->

                <!-- Put Chat bubbles here! -->
            </div>
        </main>
        <footer class="chat-session-footer">
            <div class="chat-input">
                <textarea
                    type="text"
                    class="chat-input-textarea"
                    placeholder="Type your message here..."
                ></textarea>
                <button class="chat-input-send", id="chat-input-send" onclick="console.log('Click')">Send</button>
            </div>
        </footer>
    </div>
    <script>
        // const URL_thread = 'http://127.0.0.1:8000/api/v1/assistant/thread/';
        const ws = new WebSocket('ws://localhost:8000/api/v1/assistant/thread');
        // const user_id = "44405";
        let thread_id = '';
        let assistant_id = '';

        function fillChatBubble(message, sender) {
            let chatContainer = document.querySelector('.chat-container');
            let chatBubble = document.createElement('div');
            chatBubble.classList.add('chat-bubble');
            let chatBubbleSender = document.createElement('div');
            if (sender === 'user') {
                chatBubbleSender.classList.add('chat-bubble-user');
            } else {
                chatBubbleSender.classList.add('chat-bubble-ai');
            }
            chatBubbleSender.innerHTML = `
                <p class="font-semibold">${sender === 'user' ? 'User' : 'TraderAI Assistant'}:</p>
                <p class="text-sm">${message}</p>
            `;
            chatBubble.appendChild(chatBubbleSender);
            chatContainer.appendChild(chatBubble);
        }

        ws.onopen = function(event) {
            console.log("Connection established");
        };
        ws.onmessage = function(event) {
            console.log("Message received: ", event.data);
            let data
            data = JSON.parse(event.data);
            thread_id = data.thread_id;
            assistant_id = data.assistant_id;
            assistant_answer_json = data.coder_assistan_answer;
            is_there_code = assistant_answer_json.is_there_code
            assistant_answer = assistant_answer_json.coder_assistan_answer
            // assistant_answer = "Thread ID: " + thread_id + " Assistant ID: " + assistant_id;
            fillChatBubble(assistant_answer, 'ai');
        };
        
        // On send button click
        document.getElementById('chat-input-send').addEventListener('click', function() {
            let userMessage = document.querySelector('.chat-input-textarea').value;
            fillChatBubble(userMessage, 'user');
            document.querySelector('.chat-input-textarea').value = '';
            const queryThread  = {
                "message": userMessage,
                "thread_id": thread_id,
                "assistant_id": assistant_id

            };
            console.log("Type of json: ", typeof(queryThread ));
            console.log("JSON: ", queryThread );
            // Send message to server
            ws.send(JSON.stringify(queryThread));
        });
    </script>
</body>
</html>
"""