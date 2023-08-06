from gym.envs.registration import register

register(
    id='jzx_env-v0',
    entry_point='jzx_env.envs:JzxEnv',
)