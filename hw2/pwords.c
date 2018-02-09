#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <pthread.h>

/* Dictionary struct holds a single word and a count, it points to the next word in the list. */
typedef struct dict {
  char *word;
  int count;
  struct dict *next;
} dict_t;

pthread_mutex_t mutex;
pthread_mutex_t wordmut;
/* infile and main dictionary are global now. */
FILE *infile;
dict_t* wd;

/* Allocate a word */
char *
make_word( char *word ) {
  return strcpy( malloc( strlen( word )+1 ), word );
}

/* Construct a dict with an input word. */
dict_t *
make_dict(char *word) {
  dict_t *nd = (dict_t *) malloc( sizeof(dict_t) );
  nd->word = make_word( word );
  nd->count = 1;
  nd->next = NULL;
  return nd;
}

void
insert_word(char* word) {
  
  //   Insert word into the main dict or increment count if already there
  //   return pointer to the updated dict
  
  dict_t *nd;
  dict_t *pd = NULL;		// prior to insertion point 
  dict_t *di=wd;		// following insertion point
  // Search down list to find if present or point of insertion
  while(di && ( strcmp(word, di->word ) >= 0) ) { 
    if( strcmp( word, di->word ) == 0 ) { 
      di->count++;		// increment count 
      return;			// return
    }
    pd = di;			// advance ptr pair
    di = di->next;
  }
  nd = make_dict(word);		// not found, make entry 
  nd->next = di;		// entry bigger than word or tail 
  if (pd) {
    pd->next = nd;
    return;
  }
  wd=nd;
  return;
}

/* iterate through the dict and print the list. */
void print_dict(void) {
  while (wd) {
    printf("[%d] %s\n", wd->count, wd->word);
    wd = wd->next;
  }
}

/* Gets another word. note fgetc remembers position, so after we exit this function the next call will continue from where it left off. */
int
get_word( char *buf) {
  int inword = 0;
  int c;  
  while( (c = fgetc(infile)) != EOF ) {
    if (inword && !isalpha(c)) {
      buf[inword] = '\0';	// terminate the word string
      return 1;
    } 
    if (isalpha(c)) {
      buf[inword++] = c;
    }
  }
  return 0;			// no more words
}

#define MAXWORD 1024
#define NUMTHREADS 4

/* My thread function. */
void*
thread_stuff(void* arg){
  char word[MAXWORD];
  int okgo=1;

  while (okgo){
    pthread_mutex_lock(&wordmut);
    okgo=get_word(word);
    pthread_mutex_unlock(&wordmut);
    if (okgo==0) break;
    pthread_mutex_lock(&mutex);
    insert_word(word);
    pthread_mutex_unlock(&mutex);
  }
  pthread_exit(NULL);
}

/* Not these threads are of the "join" type. */
void
words() {
  wd = NULL;
  pthread_t threads[NUMTHREADS];
  pthread_attr_t attr;
  int i;
  int t_ret;

  /*create attribute to make joinable threads*/
   pthread_attr_init(&attr);
   pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);
  /*initialize mutex */
  pthread_mutex_init(&mutex, NULL);
  pthread_mutex_init(&wordmut, NULL);
  /* make threads */
  
  for (i=0; i<NUMTHREADS; i++){
    t_ret = pthread_create(&threads[i],&attr,thread_stuff,NULL);
    if (t_ret){
      exit(-1);
    }
  }

  /* Wait on the other threads */
  for(i=0; i<NUMTHREADS; i++)
  {
     pthread_join(threads[i], NULL);
  }

  /* destroy mutex and attr*/
  pthread_mutex_destroy(&mutex);
  pthread_mutex_destroy(&wordmut);
  pthread_attr_destroy(&attr);
}

int
main( int argc, char *argv[] ) {
  wd = NULL;
  infile = stdin;
  if (argc >= 2) {
    infile = fopen (argv[1],"r");
  }
  if( !infile ) {
    printf("Unable to open %s\n",argv[1]);
    exit( EXIT_FAILURE );
  }

  words();
  print_dict();
  fclose( infile );
}
