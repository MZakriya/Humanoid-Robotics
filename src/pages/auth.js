import React, { useState } from 'react';
import Layout from '@theme/Layout';
import AuthForm from '../components/AuthForm/AuthForm';

export default function AuthPage() {
  const [mode, setMode] = useState('login'); // Default to login

  return (
    <Layout title="Authentication" description="Sign in or sign up to access personalized content">
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '80vh',
        padding: '20px'
      }}>
        <div style={{
          maxWidth: '500px',
          width: '100%',
          padding: '30px',
          border: '1px solid #ddd',
          borderRadius: '8px',
          backgroundColor: '#1a1a1a'
        }}>
          <AuthForm mode={mode} />
          <div style={{ marginTop: '20px', textAlign: 'center' }}>
            <button
              onClick={() => setMode(mode === 'login' ? 'signup' : 'login')}
              style={{
                background: 'none',
                border: 'none',
                color: '#4B0082',
                cursor: 'pointer',
                textDecoration: 'underline'
              }}
            >
              {mode === 'login'
                ? 'Need an account? Sign up'
                : 'Already have an account? Sign in'}
            </button>
          </div>
        </div>
      </div>
    </Layout>
  );
}