# labyrinth-resolution-with-pNS-neurons
Labyrinth resolution with pseudo Navier-Stokes neurons
Extraction of a hard constrained neural network from pseudo Navier Stokes equations. Application to labyrinth resolution.

To test the labyrinth_Navier_solver you can use a labyrinth generator as your convenience. This labyrinth generator is based on Wilson Algorithm in order to have an uniform distribution (very important in machine learning). However the labgen will create a database file without the start nor the end of the labyrinth. You need to make sure in the labyrinth_Navier_solver code to put an accessible END position (the (1,1) position is always accessible and by default is the START position).

You'll need matplotlib library so as to visualise the trajectory of the agent.

I've said in my report I would put online the database with 25k labyrinths but the file is too big to put it on github. So I put an other file with labyrinths with different dimensions. You can obviously use the generator to create other labyrinths.

My mail address if you have questions or if anything doesn't work correctly: nicolas.yax@ens-paris-saclay.fr
