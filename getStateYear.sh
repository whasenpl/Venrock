#!/bin/bash

echo "Extracting the state from DocGraph-Procedure.csv"
echo "./extractState.py DocGraph-Procedure.csv Procedure_$1.csv $1"
./extractState.py DocGraph-Procedure.csv Procedure_$1.csv $1
echo "Aggregating stats from the reduced Procedure file"
echo "./aggregateStats.py Procedure_$1.csv HCPCS_Stats_$1.csv"
./aggregateStats.py Procedure_$1.csv HCPCS_Stats_$1.csv
echo "Extracting subgraph pertaining only to the state"
echo "./getSubgraph.py Procedure_$1.csv DocGraph-$2-Edge.csv Edges_$2_$1.csv"
./getSubgraph.py Procedure_$1.csv DocGraph-$2-Edge.csv Edges_$2_$1.csv
echo "Running pagerank and calculating other graph stats"
echo "./pagerank.py Procedure_$1.csv Edges_$2_$1.csv Stats_$2_$1.csv"
./pagerank.py Procedure_$1.csv Edges_$2_$1.csv Stats_$2_$1.csv