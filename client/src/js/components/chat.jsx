import React, { useEffect } from 'react';
import { Widget, addResponseMessage } from 'react-chat-widget';
import Container from 'react-bootstrap/Container';

import 'react-chat-widget/lib/styles.css';

function ChatBot() {
  useEffect(() => {
    addResponseMessage('Welcome to this awesome chat!');
  }, []);

  const handleNewUserMessage = (newMessage) => {
    console.log(`New message incoming! ${newMessage}`);
    // Now send the message throught the backend API
    addResponseMessage(response);
  };

  return (
      <Widget
        handleNewUserMessage={handleNewUserMessage}
        title="Chat With Your Journal"
        subtitle="Chatting with This Month"
      />
  );
}

export default ChatBot;