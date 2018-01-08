import random
import gym
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam


class Agent:

    def __init__(self, state_size, action_size, gamma, epsilon, epsilon_min,
                 epsilon_decay, learning_rate, batch_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

    def update_target_model(self):
        # copy weights from model to target_model
        self.target_model.set_weights(self.model.get_weights())

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = self.model.predict(state)
            if done:
                target[0][action] = reward
            else:
                a = self.model.predict(next_state)[0]
                t = self.target_model.predict(next_state)[0]
                target[0][action] = reward + self.gamma * t[np.argmax(a)]
            self.model.fit(state, target, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

    def train(self, env):
        done = False
        e = 0

        while True:
            e += 1
            state = env.reset()
            state = np.reshape(state, [1, self.state_size])

            for time in range(500):
                # env.render()

                action = self.act(state)
                next_state, reward, done, _ = env.step(action)
                next_state = np.reshape(next_state, [1, self.state_size])
                self.remember(state, action, reward, next_state, done)
                state = next_state
                if done:
                    self.update_target_model()
                    print("episode: {}, score: {}, e: {:.2}".format(
                        e, time, self.epsilon
                    ))
                    break
            if len(self.memory) > self.batch_size:
                self.replay(self.batch_size)


if __name__ == '__main__':
    import snake_env

    env = gym.make('SnakeGame-v0')
    state_size = env.BOARD
    action_size = env.RANGE

    agent = Agent(
        state_size=state_size,
        action_size=action_size,
        # Discount rate.
        gamma=0.95,
        # Exploration rate.
        epsilon=15.0,
        epsilon_min=0.01,
        epsilon_decay=0.99,
        learning_rate=0.005,
        batch_size=32,
    )
    agent.train(env)
