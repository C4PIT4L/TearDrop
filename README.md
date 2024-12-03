


![Teardrop Attack](https://img.shields.io/badge/Teardrop-Attack-red?style=for-the-badge&logo=python&logoColor=white)




# TearDrop Attack

Teardrop Attack Simulation is a Python-based tool that simulates the classic Teardrop DoS attack by crafting and sending fragmented IP packets with overlapping or incorrect offsets. The attack, historically effective on older systems, causes instability or crashes by exploiting flaws in packet reassembly.



![Logo](https://images.pond5.com/teardrop-attack-isometric-icon-vector-illustration-265142275_iconl_nowm.jpeg)



## Installation



```bash
# Clone the repository
git clone https://github.com/C4PIT4L/TearDrop.git

# Navigate to the project directory
cd TearDrop

# Install the required Python packages
pip install -r requirements.txt
```
## Running the attack

Clone the project

```bash
  git clone https://github.com/C4PIT4L/TearDrop.git
  cd TearDrop
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Run the attack

```bash
  python teardrop.py <target_ip> [payload_size] [--frag_overlap_offset OFFSET] [--packet_size SIZE] [--indefinite] [--proxy PROXY]
```


## Authors

- [@C4PIT4L](https://www.github.com/C4PIT4L)

