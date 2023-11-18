git clone https://github.com/OpenMathLib/OpenBLAS.git
cd OpenBLAS
make clean
make USE_OPENMP=1
sudo make install
sudo echo "/etc/ld.so.conf.d/openblas.conf"> /etc/ld.so.conf.d/openblas.conf
sudo ldconfig
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
