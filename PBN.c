#include <stdio.h>
#include <stdlib.h>
#include <time.h>

/* aがコンスタント関数かどうかを判断する関数 */
/* コンスタント関数なら1、そうでないなら0 */
/* コンスタント関数は、入力に関わらず常に同じ値を出力するものなので
リストの最初とn番目までを比較し、不一致があったら0、全て同じなら1 */
int cnstfunc(int * a, int n) {
  int x = a[0];
  int i;
  for (i = 0; i < n; i++)
    if(a[i] != x) return 0;
  return 1;
}

/* 2進数表記のstateを10進数に変換し出力する関数 */
int encode(int * state, int node) {
  int i, n;
  n = 0;
  for (i = 0; i < node; i++) {
    n = n * 2;
    n += state[i]; 
  }
  return n;
}

/* iをnodeビットの2進数表記にしstateにいれる関数 */
void decode(int * state, int i, int node) {
  int n = 0;
  if (node >= 7) state[n++] = i / 64;
  if (node >= 6) state[n++] = (i % 64) / 32;
  if (node >= 5) state[n++] = (i % 32) / 16;
  if (node >= 4) state[n++] = (i % 16) / 8;
  state[n++] = (i % 8) / 4;
  state[n++] = (i % 4) / 2;
  state[n++] = i % 2;
}

int main() {
  char c;
  int node, degree, cnst;
  int i, j, k, n, tmp, count, funcnum, stateint;
  int topology[7][4] = {};
  int ** func;
  int *state, *oldstate;
  int *check;

  /* アトラクタ数を数える */
  int count2 = 0;
  /* 確率 */
  int p;
  /* 確率を読み取るためのもの */
  char buf[100];
  char *pointa;

  srand((unsigned int)time(NULL));

  /* 入力されたノード数を読み取る */
  /* 決めた範囲内の数値が渡されるまで繰り返す */
  while (1) {
    printf("ノード数(4~7)を入力してください...");
    /* getcharで入力の読み取り */
    c = getchar();
    /* atoiで整数化してnodeへ */
    node = atoi(&c);
    /* 決めた範囲(今回は4~7)なら */
    if (4 <= node && node <= 7) {
      /* 改行まですべて読み飛ばす */
      while ((c = getchar()) != '\n');
      /* 改行がきたら無限ループを抜ける */
      break;
    }
    /* 決めた範囲以外の入力なら、読み飛ばす */
    while ((c = getchar()) != '\n');
  }

  /* ノードの次数(入力数)を読み取る */
  /* 決めた範囲内の数値が渡されるまで繰り返す */
  while (1) {
    /* 標準入力をリセット(よくわからん) */
    rewind(stdin);
    printf("ノードの次数(2~4)を入力してください...");
    /* getcharで入力の読み取り */
    c = getchar();
    /* atoiで整数に変換してdegreeへ */
    degree = atoi(&c);
    /* 決めた範囲(今回は2~4)なら */
    if (2 <= degree && degree <= 4) {
      /* 改行まですべて読み飛ばす */
      while ((c = getchar()) != '\n');
      /* 改行が来たら無限ループを抜ける */
      break;
    }
    /* 決めた範囲以外の入力なら、読み飛ばす */
    while ((c = getchar()) != '\n');
  }

  /* コンスタント関数の有無の読み取り */
  /* 決めた数値が渡されるまで繰り返す */
  while (1) {
    printf("コンスタント関数の有無(0:無し, 1:有り)を設定してください...");
    /* getcharで入力の読み取り */
    c = getchar();
    /* atoiで整数に変換しcnstへ */
    cnst = atoi(&c);
    /* 決めた数値(今回は0か1)なら */
    if (cnst == 0 || cnst == 1) {
      /* 改行まですべて読み飛ばす */
      while ((c = getchar()) != '\n');
      /* 改行が来たら無限ループを抜ける */
      break;
    }
    /* 決めた数値以外の入力なら、読み飛ばす */
    while ((c = getchar()) != '\n');
  }

  /* 確率の読み取り */
  /* 0~100の間の整数を読み取る */
  while (1) {
    printf("関数の出力が1となる確率(%%)を入力してください...");
    /* ポインタに配列を与える */
    pointa = buf;
    /* 改行かEOFが現れるまで、配列に入力をひとつずつメモ */
    while ((c = getchar()) != '\n' && c != EOF) {
      *pointa++ = c;
    }
    /* 文字列を整数化してpに入れる */
    p = atoi(&buf[0]);
    /* 確率として正しい範囲ならぬける */
    if (p >= 0 && p <= 100) break;
    /* 改行まで読み飛ばして、もう一度 */
    while ((c = getchar()) != '\n');
  }
  
  /* 関数を決めて表示するまでを行う */
  /* 文字化けしてよくわからないので、それっぽい言葉をプリント */
  printf("\nブール関数をランダムに決定します\n\n");
  /* nodeの数だけint*確保(funcがint**であることに注意) */
  func = malloc(sizeof(int*) * node);
  /* 以下、funcを埋めていく作業 */
  /* funcには各ノードの出力が入る */
  /* func[i][j]には、i-1番目のノードに10進数でjとなる入力が入った時の出力
  例えば、次数が2の時に、2番目のノードに2進数10が入るときの出力はfunc[1][2] */
  n = 1;
  /* 次数の数の回数2倍する */
  /* n = 2^degree になる */
  /* ノードへの入力数が次数なので、degreeビットを表現するには
  2^degree  */
  for (i = 0; i < degree; i++)
    n = n * 2;
  /* funcの要素それぞれにnの数だけintを確保 */
  for (i = 0; i < node; i++)
    func[i] = malloc(sizeof(int) * n);
  /* funcに01をランダムに入れる */
  for (i = 0; i < node; i++) {
    for (j = 0; j < n; j++) {
			/* pで受け取った確率により01を決める */
			if (rand() % 100 < p) func[i][j] = 1;
			else func[i][j] = 0;
    }
    /* コンスタント関数を使わない(cnst==0)かつ
    生成したfuncがコンスタント関数(cnstfunc(func[i],n)==1)
    ならiを減らしてもう一度funcを作る */
    if (cnst == 0 && cnstfunc(func[i], n) == 1)
      i--;
  }
  /* ノードの次数を表示 */
  for (i = 0; i < degree; i++)
    printf("%d ", i+1);
  /* 仕切り */
  printf("|");
  /* ノードの数をABCDで表示 */
  for (i = 0; i < node; i++)
    /* 1つ目のノードがA、2つ目のノードに￥がB… */
    printf(" %c", i+'A');
  printf("\n");
  /* degreeビットの時の全パターンを表示しつつ、
  それぞれのときの関数を表示する */
  for (i = 0; i < n; i++){
    /* 次数が4以上の時の下から4番目のビット */
    if (degree >= 4)printf("%d ", i/8);
    /* 次数が3以上の時の下から3番目のビット */
    if (degree >= 3)printf("%d ", (i%8)/4);
    /* 下から2番目のビット */
    printf("%d ", (i%4)/2);
    /* 一番下のビット */
    printf("%d ", i%2);
    /* 仕切りを表示 */
    printf("|");
    /* 各ノードの出力を表示 */
    for (j = 0; j < node; j++) {
      /* j番目のノードに10進数でiの入力が入った時の出力がfunc[j][i] */
      printf(" %d", func[j][i]);
    }
    printf("\n");
  }
  printf("\nEnterを押すと次を実行します");
  /* Enterの読み取り */
  getchar();

  /* それぞれのノードの入力がどのノードから来るのかをランダムに決める */
  printf("それぞれのノードの入力がどのノードから来るのかを表示(トポロジーの決定)\n\n");
  printf("  |");
  for (i = 0; i < degree; i++)
    /* 何番目の入力化を表示 */
    printf(" %d", i+1);
  printf("\n");
  for (i = 0; i < node; i++) {
    /* ノードを順にA,B,C,… */
    printf("%c |", 'A'+i);
    for (j = 0; j < degree; j++) {
      /* 一つの入力に対し、きちんと決まるまで無限ループ */
      while (1) {
        /* nodeで割るあまりでノードを分類 */
	      tmp = rand() % node;
	      for (k = 0; k < j; k++)
          /* 1つのノードへ同じノードから2つ以上の入力が来てはいけないので
          被りがあれば途中で抜ける */
	        if (topology[i][k] == tmp) break;
        /* 被り無し(k==j)であれば */
	      if (k == j) {
          /* topologyへtmpを入れる */
	        topology[i][j] = tmp;
          /* tmpを元に、入力されるノードを表示 */
	        printf(" %c", 'A'+tmp);
	        break;
	      }
      }
    }
    printf("\n");
  }
  printf("\nEnterを押すと次を実行します");
  /* Enterの読み取り */
  getchar();
  
  /* ノードの初期状態を変え全パターンを調べ表示する */
  printf("ネットワークを動作させます\n\n");
  n = 1;
  /* n=2^nodeとする */
  for (i = 0; i < node; i++)
    n = n * 2;
  /* int容量をノード数だけ確保 */
  state = malloc(sizeof(int) * node);
  oldstate = malloc(sizeof(int) * node);
  /* int容量をn=2^nodeだけ確保 */
  check = malloc(sizeof(int) * n);
  /* checkを初期化 */
  for (i = 0; i < n; i++)
    check[i] = 0;
  count = 1;
  /* ノードの初期状態1つ1つについて見ていく */
  /* iの2進数表記が各ノードの01に対応する */
  for (i = 0; i < n; i++) {
    /* 現在のノードの状態を10進数で表したもの */
    stateint = i;
    /* oldstateにiを2進数で書き込む */
    decode(oldstate, i, node);
    /* 既出の状態ならcontinue */
    if (check[stateint] != 0) continue;
    /* 新出のスタートなら、いくつ目のスタートかを表示 */
    printf("(%d) ", count);
    /* 既出のノード状態になるまで無限ループ */
    while (1) {
      /* 既出のノード状態になればすぐに抜ける */
      if (check[stateint] != 0) break;
      /* checkに何番目かをいれる */
      check[stateint] = count;
      /* ノード状態を表示 */
      for (j = 0; j < node; j++) {
	      printf("%d", oldstate[j]);
      }
      /* 矢印 */
      printf("->");
      /* つぎのノード状態を計算する */
      /* funcnumは、ノードjへの入力を2進数で表したものの10進数 */
      for (j = 0; j < node; j++) {
        /* funcnumを初期化 */
	      funcnum = 0;
	      for (k = 0; k < degree; k++) {
          /* 2進数として次の位になるよう2倍する */
	        funcnum = funcnum * 2;
          /* topologyをもとにノードjの入力kになるノード状態をfuncnumにいれる */
	        funcnum += oldstate[topology[j][k]];
	      }
        /* funcを元にノードjの次の状態をstate[j]にメモ */
	      state[j] = func[j][funcnum];
      }
      /* oldstateにstateをコピー */
      for (j = 0; j < node; j++) {
	      oldstate[j] = state[j];
      }
      /* stateは2進数表記なので、10進数に変換してstateintへ入れる */
      stateint = encode(state, node);
    }
    /* oldstateを表示 */
    for (j = 0; j < node; j++) {
      printf("%d", oldstate[j]);
    }
    /* どこと同じ状態になるかを表示 */
    printf("(%d)\n", check[stateint]);
    /* 新しいアトラクタならcount2を一つ進める */
    if (check[stateint] == count) count2++;
    /* countを1つ進める */
    count++;
  }
  printf("\n");
  printf("アトラクタ数: %d\n", count2);
  return 0;
}