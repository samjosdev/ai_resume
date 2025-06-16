from fastapi import FastAPI, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sidekick_personal import SideKick
import json
import asyncio
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store active sidekick instances
active_sidekicks = {}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    logger.info("New WebSocket connection request")
    await websocket.accept()
    logger.info("WebSocket connection accepted")
    
    try:
        # Initialize Sidekick
        logger.info("Initializing Sidekick")
        sidekick = SideKick()
        await sidekick.setup()
        active_sidekicks[websocket] = sidekick
        logger.info("Sidekick initialized successfully")
        
        while True:
            # Receive message from client
            logger.info("Waiting for message from client")
            data = await websocket.receive_text()
            logger.info(f"Received raw message: {data}")
            message_data = json.loads(data)
            logger.info(f"Parsed message data: {message_data}")
            
            # Process message with Sidekick
            history = message_data.get("history", [])
            message = message_data.get("message", "")
            logger.info(f"Processing message: {message}")
            logger.info(f"With history: {history}")
            
            try:
                # Run the sidekick with default success criteria
                results = await sidekick.run_superstep(message, "The answer should be clear and accurate", history)
                logger.info(f"Sidekick results: {results}")
                
                # Send response back to client
                response_data = {
                    "type": "response",
                    "data": results
                }
                logger.info(f"Sending response: {response_data}")
                await websocket.send_json(response_data)
                logger.info("Response sent to client")
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}", exc_info=True)
                await websocket.send_json({
                    "type": "error",
                    "data": str(e)
                })
            
    except Exception as e:
        logger.error(f"Error in WebSocket connection: {str(e)}", exc_info=True)
    finally:
        # Cleanup
        if websocket in active_sidekicks:
            sidekick = active_sidekicks.pop(websocket)
            sidekick.cleanup()
        await websocket.close()
        logger.info("WebSocket connection closed")

@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    message = data.get("message", "")
    history = data.get("history", [])
    sidekick = SideKick()
    await sidekick.setup()
    try:
        results = await sidekick.run_superstep(message, "The answer should be clear and accurate", history)
        return JSONResponse({"response": results})
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        return JSONResponse({"response": f"Error: {str(e)}"}, status_code=500)
    finally:
        sidekick.cleanup()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 