import React, { useState, useEffect } from 'react';
import { useApp, render, Box, Text } from 'ink';
import TextInput from 'ink-text-input';

const EXIT = '/exit';

const App = () => {
  const { exit } = useApp();
  const [status, setStatus] = useState('Getting ready...');
  const [query, setQuery] = useState('');
  const [history, setHistory] = useState([]);

  // mock agent status
  useEffect(() => {
    const timer = setTimeout(() => setStatus('Online'), 2500);
    return () => clearTimeout(timer);
  }, []);

  const handleQuery = async (text) => {
    const cleanText = text.trim().toLowerCase();
    if (!cleanText) return;
    if (cleanText === EXIT) {
      exit();
      return;
    }

    const userMessage = { id: Date.now(), text: text, sender: 'user' };
    setHistory((prev) => [...prev, userMessage]);
    setQuery('');

    setStatus("Waiting for response...");
    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({text: text}),
      });

      const data = await response.json();

      const agentMessage = {
        id: Date.now() + 1,
        text: data.reply,
        sender: 'agent',
      };
      setHistory((prev) => [...prev, agentMessage]);

    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Error: could not connect to agent.',
        sender: 'system'
      }
      setHistory((prev) => [...prev, errorMessage]);

    } finally {
      setStatus('Online');
    }
  };

  return (
    <Box
      borderStyle="round"
      borderColor="green"
      padding={1}
      flexDirection="column"
    >
      <Text>Status</Text>
      <Text color={status === 'Online' ? 'green' : 'yellow'}>{status}</Text>

      <Box flexDirection="column" padding={1}>
        {history.map((msg) => {
          let prefix = '';
          let color = 'white';

          if (msg.sender === 'user') {
            prefix = 'You: ';
            color = 'cyan';
          } else if (msg.sender === 'agent') {
            prefix = 'Agent: ';
            color = 'green';
          } else if (msg.sender === 'system') {
            prefix = 'System: ';
            color = 'red';
          }
          return (
            <Text key={msg.id} color={color}>
              <Text bold>{prefix}</Text>
              {msg.text}
            </Text>
          );
        })}
      </Box>

      <Box>
        <Text color="cyan"> {'>'} </Text>
        <TextInput value={query} onChange={setQuery} onSubmit={handleQuery} />
      </Box>
      <Text dimColor>type '{EXIT}' to exit.</Text>
    </Box>
  );
};

render(<App />);
