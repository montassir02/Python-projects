import tensorflow as tf
import keras
import numpy as np

# 1 hidden layers
#model=keras.Sequential([keras.layers.Dense(units=1,input_shape=[1])])
# 3 hidden layers
model=tf.keras.models.Sequential([keras.layers.Dense(units=1,input_shape=[1])
                                ,keras.layers.Dense(units=1)
                                ,keras.layers.Dense(units=1)
                                  ])
model.compile(optimizer='sgd',loss='mean_squared_error')
xs=np.array([-1.0,0.0,1.0,2.0,3.0,4.0,])
ys=np.array([-3.0,-1.0,1.0,3.0,5.0,7.0,])
model.fit(xs,ys,epochs=100)
print(model.predict([10.0]))