from stable_baselines3.common.callbacks import BaseCallback
import time

class TrainingLogger(BaseCallback):
    def __init__(self, logger_timestpes = 1000):
        super().__init__()
        self.start_time = time.time()
        self.logger_timestpes = logger_timestpes

    def _on_step(self):
        if self.num_timesteps % self.logger_timestpes == 0:
            print(f"[TIMESTEP] - {self.num_timesteps} - Completed")
        return True

    def _on_training_end(self):
        elapsed = (time.time() - self.start_time)
        print("\n========================")
        print("Training Finished")
        print(f"Time Taken: {elapsed:.2f} sec")