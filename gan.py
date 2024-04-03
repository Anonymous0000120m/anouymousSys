import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

# 定义生成器网络
def build_generator(latent_dim):
    model = models.Sequential([
        layers.Dense(128, input_dim=latent_dim, activation='relu'),
        layers.Dense(784, activation='sigmoid'),
        layers.Reshape((28, 28, 1))
    ])
    return model

# 定义判别器网络
def build_discriminator(input_shape):
    model = models.Sequential([
        layers.Flatten(input_shape=input_shape),
        layers.Dense(128, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    return model

# 定义生成对抗网络
def build_gan(generator, discriminator):
    discriminator.trainable = False
    model = models.Sequential([
        generator,
        discriminator
    ])
    return model

# 加载MNIST数据集
(train_images, _), (_, _) = tf.keras.datasets.mnist.load_data()
train_images = train_images.astype('float32') / 255

# 定义训练参数
latent_dim = 100
batch_size = 128
epochs = 10000

# 构建并编译生成器和判别器
generator = build_generator(latent_dim)
discriminator = build_discriminator(train_images[0].shape)
gan = build_gan(generator, discriminator)
gan.compile(loss='binary_crossentropy', optimizer='adam')

# 定义训练过程
def train_gan(generator, discriminator, gan, train_images, latent_dim, epochs, batch_size):
    for epoch in range(epochs):
        # 训练判别器
        noise = np.random.normal(0, 1, (batch_size, latent_dim))
        fake_images = generator.predict(noise)
        real_images = train_images[np.random.randint(0, train_images.shape[0], batch_size)]
        combined_images = np.concatenate([fake_images, real_images])
        labels = np.concatenate([np.zeros((batch_size, 1)), np.ones((batch_size, 1))])
        labels += 0.05 * np.random.random(labels.shape)  # 添加随机噪声
        discriminator_loss = discriminator.train_on_batch(combined_images, labels)

        # 训练生成器
        noise = np.random.normal(0, 1, (batch_size, latent_dim))
        misleading_labels = np.ones((batch_size, 1))
        generator_loss = gan.train_on_batch(noise, misleading_labels)

        # 每100个epoch输出一次结果
        if epoch % 100 == 0:
            print(f'Epoch: {epoch}, Generator Loss: {generator_loss}, Discriminator Loss: {discriminator_loss}')

# 训练GAN模型
train_gan(generator, discriminator, gan, train_images, latent_dim, epochs, batch_size)
