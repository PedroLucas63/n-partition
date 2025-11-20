#include "Partition.hpp"
#include <bits/stdc++.h>
#include <getopt.h>

using namespace std;
using namespace partition; // ValueType vem daqui

static std::mt19937_64 rng((std::random_device())());

ValueType sum_vector(const vector<ValueType> &v) {
  ValueType s = 0;
  for (auto x : v)
    s += x;
  return s;
}

template <size_t N>
ValueType compute_makespan_array(const array<vector<ValueType>, N> &groups) {
  ValueType best = 0;
  for (const auto &g : groups) {
    ValueType s = sum_vector(g);
    if (s > best)
      best = s;
  }
  return best;
}

ValueType call_CGA_and_get_makespan(int n, vector<ValueType> &arr) {
  switch (n) {
  case 2:
    return compute_makespan_array(CGA<2>(arr));
  case 3:
    return compute_makespan_array(CGA<3>(arr));
  case 4:
    return compute_makespan_array(CGA<4>(arr));
  case 5:
    return compute_makespan_array(CGA<5>(arr));
  case 8:
    return compute_makespan_array(CGA<8>(arr));
  default:
    throw runtime_error("Unsupported n");
  }
}

pair<ValueType, vector<ValueType>> balanced_strategy(int n, int m, int b) {
  // lb pode ficar grande; usamos uint64_t temporário para distribuição
  uint64_t lb = (b >= 64) ? 0 : (1ULL << (b - 1));
  lb = lb * static_cast<uint64_t>(m);
  std::uniform_int_distribution<uint64_t> uni(lb, 2 * lb);
  uint64_t total_sum = uni(rng);

  int q = m / n;
  int r = m % n;
  uint64_t group_sum_u = total_sum / static_cast<uint64_t>(n);
  ValueType group_sum = static_cast<ValueType>(group_sum_u);

  vector<ValueType> values;
  values.reserve(m);

  for (int gi = 0; gi < n; gi++) {
    int gsz = (r > 0 ? q + 1 : q);
    if (r > 0)
      --r;

    uint64_t remaining = group_sum_u;

    for (int i = 0; i < gsz; i++) {
      if (i == gsz - 1) {
        ValueType v = static_cast<ValueType>(remaining);
        if (v < 1)
          v = 1;
        values.push_back(v);
      } else {
        uint64_t max_pick = (remaining > static_cast<uint64_t>(gsz - i - 1))
                                ? (remaining - (gsz - i - 1))
                                : 1ULL;
        std::uniform_int_distribution<uint64_t> d(1, max_pick);
        uint64_t chosen = d(rng);
        values.push_back(static_cast<ValueType>(chosen));
        remaining -= chosen;
      }
    }
  }

  shuffle(values.begin(), values.end(), rng);
  return {group_sum, values};
}

pair<ValueType, vector<ValueType>> random_strategy(int n, int m, int b) {
  uint64_t max_val = (b >= 63) ? UINT64_MAX : ((1ULL << b) - 1ULL);
  std::uniform_int_distribution<uint64_t> dist(1, max_val);

  vector<ValueType> values;
  values.reserve(m);
  for (int i = 0; i < m; i++)
    values.push_back(static_cast<ValueType>(dist(rng)));

  vector<ValueType> tmp = values;
  ValueType makespan = call_CGA_and_get_makespan(n, tmp);

  return {makespan, values};
}

//
// ================== CLI =======================
//
struct CLIConfig {
  string outfile = "";
  string strategy = "balanced";
};

CLIConfig parse_cli(int argc, char **argv) {
  CLIConfig cfg;

  const struct option long_opts[] = {{"file", required_argument, 0, 'f'},
                                     {"strategy", required_argument, 0, 's'},
                                     {0, 0, 0, 0}};

  while (true) {
    int opt = getopt_long(argc, argv, "f:s:", long_opts, nullptr);
    if (opt == -1)
      break;

    switch (opt) {
    case 'f':
      cfg.outfile = optarg;
      break;

    case 's':
      cfg.strategy = optarg;
      if (cfg.strategy != "balanced" && cfg.strategy != "random") {
        cerr << "Invalid strategy. Use balanced or random.\n";
        exit(1);
      }
      break;

    default:
      cerr << "Unknown option\n";
      exit(1);
    }
  }

  if (cfg.outfile.empty()) {
    cerr << "You must provide --file <path>\n";
    exit(1);
  }

  return cfg;
}

void progress_bar(size_t current, size_t total, size_t bar_width = 40) {
  double ratio = total == 0 ? 1.0 : double(current) / double(total);
  size_t filled = size_t(ratio * bar_width);

  cout << "\r[";
  for (size_t i = 0; i < bar_width; ++i) {
    cout << (i < filled ? "#" : "-");
  }
  cout << "] ";
  cout << setw(3) << (int)round(ratio * 100.0) << "% (" << current << "/"
       << total << ")";
  cout.flush();
}

//
// =================== Helpers ======================
//
int max_m_for_n(int n) {
  switch (n) {
  case 2:
    return 35;
  case 3:
    return 30;
  case 4:
    return 25;
  case 5:
    return 20;
  case 8:
    return 16;
  default:
    return 0;
  }
}

//
// =================== MAIN ======================
//
int main(int argc, char **argv) {
  // usa parse_cli para --file e --strategy
  CLIConfig cfg = parse_cli(argc, argv);
  string strategy = cfg.strategy;
  string out_filename = cfg.outfile;

  // --- Arquivo ---
  ofstream fout(out_filename);
  if (!fout.is_open()) {
    cerr << "Failed to open output file: " << out_filename << "\n";
    return 1;
  }

  // --- Precomputação do total ---
  vector<int> n_values = {2, 3, 4, 5, 8};
  vector<int> b_values = {4, 8, 16, 32};
  int repetitions = 5;

  size_t total_instances = 0;
  for (int n : n_values) {
    int maxm = max_m_for_n(n);
    for (int m = n; m <= maxm;) {
      for (int b : b_values)
        total_instances += repetitions;
      if (m < 20) {
        m++;
      } else {
        m += 5;
      }
    }
  }

  size_t prog = 0;
  int instance_id = 1;

  // --- Loop principal ---
  for (int n : n_values) {
    int maxm = max_m_for_n(n);
    for (int m = n; m <= maxm;) {
      for (int b : b_values) {
        for (int rep = 0; rep < repetitions; ++rep) {
          pair<ValueType, vector<ValueType>> result;

          if (strategy == "balanced") {
            result = balanced_strategy(n, m, b);
          } else if (strategy == "random") {
            result = random_strategy(n, m, b);
          } else {
            cerr << "Unknown strategy: " << strategy << "\n";
            return 2;
          }

          ValueType makespan = result.first;
          const vector<ValueType> &values = result.second;

          fout << "# Instance " << instance_id << "\n";
          fout << m << " " << n << " " << b << " " << makespan << "\n";
          for (size_t i = 0; i < values.size(); ++i)
            fout << values[i] << (i + 1 < values.size() ? " " : "\n");
          fout << "\n";

          ++instance_id;
          ++prog;

          // Mostrar barra de progresso
          progress_bar(prog, total_instances);
        }
      }
      if (m < 20) {
        m++;
      } else {
        m += 5;
      }
    }
  }

  cout << "\nDone! Total = " << (instance_id - 1) << "\n";
  cout << "Output file: " << out_filename << "\n";
  cout << "Strategy: " << strategy << "\n";

  return 0;
}
