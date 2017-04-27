/* Where possible, this software has been disclaimed from any copyright
   and is placed in the public domain. Where that dedication is not
   recognized, you are granted a perpetual, irrevocable license to copy
   and modify this file in any way you see fit. */

/**
 * 1. Create a guarded header that defines SKIPLIST_KEY and SKIPLIST_VALUE
 *    and includes skiplist.h. Optionally define SKIPLIST_NAMESPACE.
 * 2. Define SKIPLIST_IMPLEMENTATION somewhere in your program above
 *    your custom header include.
 * 3. Repeat for any different key/value pair types you need. Be sure to
 *    define different SKIPLIST_NAMESPACE values and define SKIPLIST_IMPLEMENTATION
 *    once for each key/value type pair.
 * 4. Other options:
 *      - SKIPLIST_MAX_LEVELS - 33 by default
 *      - SKIPLIST_MALLOC & SKIPLIST_FREE - wrappers for stdlib malloc/free by default
 *        Both are passed a void * data pointer (for memory pool, gc context, etc).
 *      - SKIPLIST_RAND & SKIPLIST_SRAND - wrappers around stdlib rand/srand.
 *        Both are passed a void * pointer for a random context.
 *      - SKIPLIST_STATIC - if defined, declare all public functions static
 *        (make skiplist local to the file it's included from).
 *      - SKIPLIST_EXTERN - 'extern' by default; define to change calling convention
 *        or linkage etc.
 *
 * Example:
 *
 *     // skiplist_str_int.h
 *     // Include this file wherever you need a string -> int skiplist
 *     #ifndef SKIPLIST_STR_INT_H
 *     #define SKIPLIST_STR_INT_H
 *     
 *     #define SKIPLIST_KEY const char *
 *     #define SKIPLIST_VALUE int
 *     #define SKIPLIST_NAMESPACE sl_strint_
 *     #include "skiplist.h"
 *
 *     #endif
 *
 *     // program.c
 *     // short test drive program
 *     #include <stdio.h>
 *     #include <string.h>
 *     #define SKIPLIST_IMPLEMENTATION
 *     #include "skiplist_str_int.h"
 *
 *     int cmp(const char *a, const char *b, void *userdata) {
 *         return strcmp(a, b);
 *     }
 *
 *     int iter(const char *key, int val, void *userdata) {
 *         printf("%s = %d\n", key, val);
 *         return 0;
 *     }
 *
 *     int main(int argc, const char **argv) {
 *         sl_strint_skiplist list;
 *         int err = sl_strint_init(&list, cmp, NULL);
 *         // Not real error handling
 *         if (err) {
 *             puts("Uh oh");
 *             exit(err);
 *         }
 *         
 *         sl_strint_insert(&list, "a", 1, NULL);
 *         sl_strint_insert(&list, "c", 3, NULL);
 *         sl_strint_insert(&list, "b", 2, NULL);
 *         
 *         short has_b = sl_strint_find(&list, "b", NULL),  // => 1
 *               has_d = sl_strint_find(&list, "d", NULL);  // => 0
 *         
 *         int a_val;
 *         short exists = sl_strint_find(&list, "a", &a_val);
 *         if (exists)
 *             printf("a = %d\n", a_val);
 *         else
 *             puts("a does not exist");
 *
 *         int default_val = 10;
 *         int d_val = sl_strint_get(&list, "d", default_val);  // => 10
 *         
 *         sl_strint_iter(&list, iter, NULL);
 *         // Prints a = 1, b = 2, c = 3
 *
 *         int b_val;
 *         short existed = sl_strint_remove(&list, "b", &b_val);
 *         if (existed)
 *             print("b used to be %d, but now it is no more\n", b_val);
 *         else
 *             puts("b was only an illusion, a fleeting glimpse of a dream");
 *         
 *         sl_strint_free(&list);
 *         return 0;
 *     }
 */
void skiplist__stdsrand(void *_userdata);
typedef int (* skiplist_cmp_fn)(uint64_t, uint64_t, void *);
typedef int (* skiplist_iter_fn)(uint64_t, void *, void *);

typedef struct skiplist__node {
    unsigned int height;
    uint64_t key;
    void * val;
    struct skiplist__node *prev;
    struct skiplist__node *next[33];
} skiplist_node;

typedef struct {
    unsigned long size;
    unsigned int highest;
    skiplist_cmp_fn cmp;
    void *cmp_udata;
    void *mem_udata;
    void *rand_udata;
    skiplist_node *head;
} skiplist_skiplist;

/* Must be called prior to using any other functions on a skiplist.
 * @list a pointer to the skiplist to initialize
 * @cmp the comparator function to use to order nodes
 * @cmp_udata Opaque pointer to pass to cmp
 * @mem_udata Opaque pointer to pass to the SKIPLIST_MALLOC and
 *            SKIPLIST_FREE macros. Unused by default, but custom
  *           memory allocators may use it.
 * @rand_udata Opaque pointer to pass to the SKIPLIST_RAND and
 *             SKIPLIST_SRAND macros. Unused by default, but custom
 *             RNGs may use it.
 *
 * @return 0 if successful and nonzero if something failed
 */

int skiplist_init(skiplist_skiplist *list, skiplist_cmp_fn cmp, void *cmp_udata, void *mem_udata, void *rand_udata);

/* Free memory used by a skiplist.
 * @list Free this guy from his bondage to memory.
 */

void skiplist_free(skiplist_skiplist *list);

/* Sets a value in the skiplist.
 * @list An initialized skiplist
 * @key Associate the value with this key
 * @val Value
 * @prior If non-NULL, put the prior value at this location. Not touched if
 *        there was no prior value associated with this key.
 *
 * If a value already exists at that key,
 * overwrite it and stick the prior value in this function's out parameter.
 *
 * @return 0 if no value was at this key, 1 if a value did exist and was
 *          overwritten.
 */

short skiplist_insert(skiplist_skiplist *list, uint64_t key, void * val, void * *prior);

/* Gets a value associated with a key.
 * @list An initialized skiplist
 * @key Get the value associated with this key
 * @out If a value exists, store it at this location.
 *      If this parameter is NULL, nothing is stored.
 *
 * @return 0 if the key does not exist, 1 if it does
 */

short skiplist_find(skiplist_skiplist *list, uint64_t key, void * *out);

/* Gets a value associated with a key, or a default value.
 * @list An initialized skiplist
 * @key Get the value associated with this key
 * @default_val If the key does not exist in this list,
 *              return this value instead.
 *
 * @return The value associated with the key or default_val if the
 *          key is not set.
 */

void * skiplist_get(skiplist_skiplist *list, uint64_t key, void * default_val);

/* Removes a key/value pair from this list.
 * @list An initialized skiplist
 * @key Key indicating the key/value pair to remove
 * @out If non-NULL and the key existed, store the old value at this location
 *
 * @return 1 if the key used to be in the list (and was thus removed),
 *          0 if it was never there
 */

short skiplist_remove(skiplist_skiplist *list, uint64_t key, void * *out);

/* Iterates through all key/value pairs in order.
 * @list An initialized skiplist
 * @iter An iterator function to call for each key/value pair
 * @userdata An opaque pointer to pass to `iter`.
 *
 * If `iter` returns a non-zero value, stop the iteration and return
 * that value.
 *
 * @return The first non-zero result of `iter` or 0 if `iter` always
 *         returned 0.
 */

int skiplist_iter(skiplist_skiplist *list, skiplist_iter_fn iter, void *userdata);

/* Does what it says on the tin.
 * @list An initialized skiplist
 *
 * @return The number of key/value pairs in the skiplist
 */

unsigned long skiplist_size(skiplist_skiplist *list);

/* Returns the minimum key and value in this list.
 * @list An initalized skiplist
 * @key_out Set to the smallest key if non-NULL and the list is not empty
 * @val_out Set to the value associated with the smallest key if non-NULL
 *          and the list is not empty.
 *
 * @return 0 if the list is empty and 1 if it is not
 */

short skiplist_min(skiplist_skiplist *list, uint64_t *key_out, void * *val_out);

/* Returns the maximum key and value in this list.
 * @list An initalized skiplist
 * @key_out Set to the largest key if non-NULL and the list is not empty
 * @val_out Set to the value associated with the largest key if non-NULL
 *          and the list is not empty.
 *
 * @return 0 if the list is empty and 1 if it is not
 */

short skiplist_max(skiplist_skiplist *list, uint64_t *key_out, void * *val_out);

/* Removes and returns the minimum key/value pair from a list.
 * @list An initialized skiplist
 * @key_out Set to the smallest key if non-NULL and the list is not empty
 * @val_out Set to the value associated with the smallest key if non-NULL
 *          and the list is not empty.
 *
 * @return 0 if the list was already empty and 1 if it was not
 */

short skiplist_pop(skiplist_skiplist *list, uint64_t *key_out, void * *val_out);

/* Removes and returns the maximum key/value pair from a list.
 * @list An initialized skiplist
 * @key_out Set to the largest key if non-NULL and the list is not empty
 * @val_out Set to the value associated with the largest key if non-NULL
 *          and the list is not empty.
 *
 * @return 0 if the list was already empty and 1 if it was not
 */

short skiplist_shift(skiplist_skiplist *list, uint64_t *key_out, void * *val_out);

int skiplist_uint64_cmp(uint64_t a, uint64_t b, void *userdata);
