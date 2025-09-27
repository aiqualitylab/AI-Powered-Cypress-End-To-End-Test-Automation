const request = require('supertest');
const app = require('../../app');

describe('POST /api/login', () => {
  const validCredentials = {
    username: 'tomsmith',
    password: 'SuperSecretPassword!'
  };

  const invalidCredentials = {
    username: 'invalidUser',
    password: 'wrongPassword'
  };

  it('should log in successfully with valid credentials', async () => {
    const response = await request(app)
      .post('/api/login')
      .send(validCredentials);
    
    expect(response.status).toBe(200);
  });

  it('should fail to log in with invalid credentials', async () => {
    const response = await request(app)
      .post('/api/login')
      .send(invalidCredentials);
    
    expect(response.status).toBe(401);
  });
});
