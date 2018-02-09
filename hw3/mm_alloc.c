/*
 * mm_alloc.c
 *
 * My implementation works essentially how Dmitry would expect it to (judging by
 * his definition of struct s_block) except for a few minor things:
 *
 *    1) I use an integer (pnt_diff) to find a block pointer in get_block. It
 *       is initialized by the first mm_malloc.
 *    2) I don't know what the data array in the struct is for, so I don't
 *       initialize it or use it.
 *    3) I don't use the fusion function, but everything it would do is done in
 *       free_block. The idea is that the memory is in a contiguous (no adjacent
 *       free blocks) state before freeing, and freeing makes sure to keep it
 *       contiguous. Thus the memory is always contiguous.
 *    4) I use a couple of my own functions as shorthand for some tasks,
 *       documentation is below with them.
 *    5) Although I can't see how you could go without it, I make use of a
 *       pointer (mm_first) to the first block in my list.
 *    6) The reason for all the somewaht pointless casting is to make warnings
 *       clearer. On that note, memcpy gives an implicit decleration warning,
 *       but all casting and assignments to variables I try doesn;t change it - 
 *       so I ignore it.
 *    7) It is not thread safe, or at least I didn't explicitly design it as
 *       such.
 *    8) Please also note that I have modified the standard test to test more.
 *       See mm_test.c for details.
 */

#include "mm_alloc.h"

#include <stdlib.h>
#include <unistd.h>

/* Your final implementation should comment out this macro. */
/* #define MM_USE_STUBS */

/* a pointer to the first block */
s_block_ptr mm_first=NULL;
/* address difference between block and block->ptr */;
intptr_t pnt_diff=0;

/* celing to a multiple of half_page size */
size_t normalize(size_t s){
  int half_page = (sysconf(_SC_PAGESIZE)/2);
  return (size_t)half_page*(((int)s+half_page-1)/half_page);
}

/* makes a new block and links up the double linked list properly. */
void block_init(s_block_ptr loc, size_t size, s_block_ptr prev, s_block_ptr next){
  loc->size=size;
  loc->next=next;
  loc->prev=prev;
  loc->free=1;
  loc->ptr=loc+BLOCK_SIZE;

  if (prev!=(s_block_ptr)NULL) prev->next=loc;
  if (next!=(s_block_ptr)NULL) next->prev=loc;
}

/* frees a block and relinks everything */
void block_free(s_block_ptr loc){
  s_block_ptr next;
  s_block_ptr prev;
  if (loc==(s_block_ptr)NULL) return;
  loc->free=1;
  loc->ptr=NULL;

  /* Is there space in front of us? */
  next = loc->next;
  if ((next!=(s_block_ptr)NULL)&&(next->free==1)){
    loc->size = loc->size + next->size;
    loc->next=next->next;
    if (next->next!=(s_block_ptr)NULL) next->next->prev = loc;
    /* Wipe next */
    next->size=0;
    next->next=(s_block_ptr)NULL;
    next->prev=(s_block_ptr)NULL;
    next->free=0;
    next->ptr=(void *)NULL;
  }
  
  /* Is there space behind us? */
  prev = loc->prev;
  if ((prev!=(s_block_ptr)NULL)&&(prev->free==1)){
    prev->size=prev->size+loc->size;
    prev->next=loc->next;
    if (loc->next!=(s_block_ptr)NULL){
      loc->next->prev=prev;
    }
    /* Wipe loc */
    loc->size=0;
    loc->next=(s_block_ptr)NULL;
    loc->prev=(s_block_ptr)NULL;
    loc->free=0;
    loc->ptr=(void *)NULL;
  }

  /* is this the last block? */
  if ((prev==(s_block_ptr)NULL)&&(next==(s_block_ptr)NULL)) mm_first=NULL;
}

void split_block(s_block_ptr b, size_t s){
  /* will split the block after size s. */
  s_block_ptr next_block = (s_block_ptr) ((intptr_t)b+(intptr_t)s);
  block_init(next_block,b->size-s,b,b->next);
  
}

s_block_ptr fusion(s_block_ptr b){
  /* block_free essentially does this. Not used. */
  return (s_block_ptr)NULL;
}

s_block_ptr extend_heap(s_block_ptr last, size_t s){
  s_block_ptr baby =(s_block_ptr) sbrk(s);
  block_init(baby,s,last,NULL);
  return baby;
}

s_block_ptr get_block(void *p){
  intptr_t addr=(intptr_t)p - pnt_diff;
  return (s_block_ptr)addr;
}

void* mm_malloc(size_t size)
{
#ifdef MM_USE_STUBS
    return calloc(1, size);
#else
  int half_page = (sysconf(_SC_PAGESIZE)/2);
  s_block_ptr first;
  s_block_ptr next = mm_first;
  s_block_ptr prev = NULL;
  /* first run? */
  if (mm_first==(s_block_ptr)NULL){
    first = (s_block_ptr) sbrk((int)normalize(size));
    block_init(first,normalize(size),NULL,NULL);
    first->free=0;
    mm_first=first;
    /* set 'seek' distance. */
    pnt_diff=(intptr_t)first->ptr - (intptr_t)first;
    return (void*)first->ptr;
  }
  /* Traverse to free with enough size */
  while (next!=(s_block_ptr)NULL){
    if ((next->free==1)&&(next->size-BLOCK_SIZE>=size)){
      next->free=0;
      /*Can we split this block? */
      if(next->size-normalize(size)>=half_page){
	split_block(next,normalize(size));
      }
      return next->ptr;
    }
    prev=next;
    next = next->next;
  }
  /* if we got here we're at the last block, so we need more room. */
  extend_heap(prev,normalize(size));
  prev->next->free=0;
  return (void*) prev->next->ptr;
#endif
}

void* mm_realloc(void* ptr, size_t size)
{
#ifdef MM_USE_STUBS
    return realloc(ptr, size);
#else
  /* get the block of ptr */
  s_block_ptr orig = get_block(ptr);
  /* get a spot */
  void* baby = mm_malloc(size);
  /* get baby block */
  s_block_ptr baby_b = get_block(baby);
  /* copy the stuff we have */
  memcpy(baby_b->ptr,orig->ptr,orig->size-BLOCK_SIZE);
  /*free original */
  mm_free(orig->ptr);
  
  return baby;

#endif
}

void mm_free(void* ptr)
{
#ifdef MM_USE_STUBS
    free(ptr);
#else
  s_block_ptr block = get_block(ptr);
  block_free(block);
  return;

#endif
}
