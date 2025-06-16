import React, { useState, useEffect, useRef } from 'react';
import styled from '@emotion/styled';
import { marked } from 'marked';

const renderer = new marked.Renderer();
renderer.link = function(tokenOrHref, title, text) {
  // If the first argument is an object (token), extract href/text/title
  let href, linkText, linkTitle;
  if (typeof tokenOrHref === 'object' && tokenOrHref !== null) {
    href = tokenOrHref.href;
    linkText = tokenOrHref.text;
    linkTitle = tokenOrHref.title;
  } else {
    href = tokenOrHref;
    linkText = text;
    linkTitle = title;
  }
  if (typeof href !== 'string') {
    console.warn('Non-string href in markdown link:', href);
    return linkText || '';
  }
  const safeHref = href.startsWith('http') ? href : `https://${href}`;
  const safeText = linkText || safeHref;
  const safeTitle = linkTitle ? ` title="${linkTitle}"` : '';
  return `<a href="${safeHref}"${safeTitle} target="_blank" rel="noopener noreferrer" class="link">${safeText}</a>`;
};

marked.setOptions({
  renderer,
  breaks: true,
  gfm: true,
  headerIds: false,
  mangle: false,
  sanitize: false,
  smartLists: true,
  smartypants: true
});

const AppContainer = styled.div`
  display: flex;
  height: 100vh;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #101112 0%, #1a1d1f 100%);
  color: #ececf1;
  font-family: 'Inter', 'Segoe UI', Arial, sans-serif;

  .link {
    color: #00ff80;
    text-decoration: underline;
    transition: color 0.2s;
    &:hover {
      color: #4ade80;
    }
  }
`;

const ChatContainer = styled.div`
  width: 100%;
  max-width: 720px;
  height: 90vh;
  background: #181c1f;
  border-radius: 16px;
  box-shadow: 0 2px 16px 0 #00000040;
  display: flex;
  flex-direction: column;
  overflow: hidden;
`;

const Header = styled.div`
  width: 100%;
  background: #23272b;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.7rem 0 1.1rem 0;
  border-bottom: 1px solid #333;
`;

const Logo = styled.img`
  width: 36px;
  height: 36px;
  margin-bottom: 1rem;
`;

const Title = styled.h1`
  color: #fff;
  font-size: 1.45rem;
  font-weight: 500;
  margin: 0;
  letter-spacing: 0.4px;
  font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
  text-align: center;
  opacity: ${props => (props.visible ? 1 : 0)};
  max-height: ${props => (props.visible ? '100px' : '0')};
  transition: opacity 0.4s, max-height 0.4s;
  overflow: hidden;
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const MessageBubble = styled.div`
  max-width: 70%;
  align-self: ${props => (props.isUser ? 'flex-end' : 'flex-start')};
  background: ${props => (props.isUser ? 'linear-gradient(135deg, #22c55e 0%, #15803d 100%)' : '#23272b')};
  color: #ececf1;
  border-radius: 16px;
  padding: 0.5rem 0.7rem;
  font-size: 0.88rem;
  font-weight: 400;
  box-shadow: 0 2px 8px 0 #00000020;
  word-break: break-word;
  line-height: 1.4;
  margin-left: ${props => (props.isUser ? 'auto' : '0')};
  margin-right: ${props => (props.isUser ? '0' : 'auto')};
  & pre, & code {
    background: #19391a;
    color: #00ff80;
    font-family: 'Fira Mono', 'Consolas', 'Menlo', monospace;
    border-radius: 8px;
    padding: 0.3em 0.5em;
    font-size: 0.85em;
    margin: 0.3em 0;
    display: block;
    overflow-x: auto;
  }
  & a, & a:visited {
    color: #00ff80 !important;
    text-decoration: underline;
    transition: color 0.2s;
  }
  & a:hover {
    color: #4ade80 !important;
    text-decoration: underline;
  }
`;

const InputBar = styled.div`
  display: flex;
  align-items: center;
  padding: 1.2rem 2rem;
  background: #181c1f;
  border-top: 1px solid #23272b;
  justify-content: center;
`;

const InputWrapper = styled.div`
  position: relative;
  flex: 1;
  display: flex;
  align-items: center;
  max-width: 750px;
`;

const Input = styled.input`
  width: 100%;
  padding: 1.1rem 3.2rem 1.1rem 1.2rem;
  border: none;
  border-radius: 24px;
  font-size: 1.05rem;
  background: #fff;
  color: #23272b;
  outline: none;
  box-shadow: 0 1px 4px 0 #00000010;
  transition: border 0.2s;
  &:focus {
    border: 1.5px solid #22c55e;
  }
`;

const ArrowButton = styled.button`
  position: absolute;
  right: 0.7rem;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #22c55e 0%, #15803d 100%);
  border: none;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.2s;
  box-shadow: 0 2px 8px 0 #00000010;
  &:hover {
    background: linear-gradient(135deg, #16a34a 0%, #166534 100%);
  }
  &:disabled {
    background: #e5e7eb;
    color: #888;
    cursor: not-allowed;
  }
`;

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [headerMinimized, setHeaderMinimized] = useState(false);
  const ws = useRef(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    ws.current = new WebSocket('ws://localhost:8000/ws');
    ws.current.onopen = () => {
      console.log('WebSocket connected');
      setIsConnected(true);
    };
    ws.current.onmessage = (event) => {
      console.log('Raw message data:', event.data);
      const data = JSON.parse(event.data);
      console.log('Parsed message data:', data);
      if (data.type === 'response' && Array.isArray(data.data)) {
        console.log('Message history:', data.data);
        const backendHistory = data.data.map(msg => {
          console.log('Processing message:', msg);
          const processed = {
            content: msg.content,
            type: msg.role === 'user' ? 'user' : 'assistant'
          };
          console.log('Processed message:', processed);
          return processed;
        });
        console.log('Final processed history:', backendHistory);
        setMessages(backendHistory);
      } else if (data.type === 'error') {
        console.error('Error from server:', data.data);
        setMessages(prev => [...prev, { content: `Error: ${data.data}`, type: 'assistant' }]);
      }
    };
    ws.current.onclose = () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
    };
    ws.current.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
    return () => ws.current && ws.current.close();
  }, []);

  const sendMessage = () => {
    if (!input.trim()) return;
    if (!ws.current || ws.current.readyState !== WebSocket.OPEN) {
      console.error('WebSocket is not connected');
      return;
    }
    const optimisticMessages = [...messages, { content: input, type: 'user' }];
    setMessages(optimisticMessages);
    setHeaderMinimized(true);
    try {
      const messageData = {
        message: input,
        history: optimisticMessages.map(m => ({ role: m.type, content: m.content }))
      };
      ws.current.send(JSON.stringify(messageData));
      setInput('');
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <AppContainer>
      <ChatContainer>
        <Header>
          <Logo src="https://upload.wikimedia.org/wikipedia/commons/4/4b/OpenAI_Logo.svg" alt="Logo" />
          <Title visible={!headerMinimized}>How can I help you today?</Title>
        </Header>
        <MessagesContainer>
          {messages.map((message, index) => {
            console.log('Rendering message:', message);
            const safeContent = typeof message.content === 'string'
              ? message.content
              : JSON.stringify(message.content);
            if (message.type === 'user') {
              return (
                <MessageBubble key={index} isUser={true}>
                  {safeContent}
                </MessageBubble>
              );
            } else {
              if (typeof message.content !== 'string') {
                console.warn('Assistant message content is not a string:', message.content);
                return (
                  <MessageBubble key={index} isUser={false}>
                    {JSON.stringify(message.content)}
                  </MessageBubble>
                );
              }
              const html = marked.parse(message.content, {
                renderer,
                breaks: true,
                gfm: true,
                headerIds: false,
                mangle: false,
                sanitize: false,
                smartLists: true,
                smartypants: true
              });
              console.log('Rendered HTML:', html);
              return (
                <MessageBubble
                  key={index}
                  isUser={false}
                  dangerouslySetInnerHTML={{ __html: html }}
                />
              );
            }
          })}
          <div ref={messagesEndRef} />
        </MessagesContainer>
        <InputBar>
          <InputWrapper>
            <Input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && sendMessage()}
              placeholder="Type your message..."
            />
            <ArrowButton onClick={sendMessage} disabled={!input.trim()} aria-label="Send">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="#fff" width="22" height="22">
                <path strokeLinecap="round" strokeLinejoin="round" d="M5 12h14M13 6l6 6-6 6" />
              </svg>
            </ArrowButton>
          </InputWrapper>
        </InputBar>
      </ChatContainer>
    </AppContainer>
  );
}

export default App;