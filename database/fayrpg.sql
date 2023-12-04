PGDMP  9    0                {            fayrpg    16.1    16.0 9    2           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            3           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            4           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            5           1262    16394    fayrpg    DATABASE     }   CREATE DATABASE fayrpg WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Hungarian_Hungary.1250';
    DROP DATABASE fayrpg;
                postgres    false            6           0    0    DATABASE fayrpg    COMMENT     (   COMMENT ON DATABASE fayrpg IS 'FayRPG';
                   postgres    false    4917                        2615    16395    fayrpg    SCHEMA        CREATE SCHEMA fayrpg;
    DROP SCHEMA fayrpg;
                postgres    false            �            1259    16468    house_types    TABLE     �   CREATE TABLE fayrpg.house_types (
    id integer NOT NULL,
    enter_x real,
    enter_y real,
    enter_z real,
    angle real,
    interior integer,
    description text,
    price integer
);
    DROP TABLE fayrpg.house_types;
       fayrpg         heap    postgres    false    5            �            1259    16430    houses    TABLE       CREATE TABLE fayrpg.houses (
    id bigint NOT NULL,
    entry_x real,
    entry_y real,
    entry_z real,
    angle real,
    owner_id bigint,
    type integer,
    locked boolean,
    interior integer,
    price bigint,
    housetype_id integer,
    rentdate date
);
    DROP TABLE fayrpg.houses;
       fayrpg         heap    postgres    false    5            �            1259    16429    houses_id_seq    SEQUENCE     v   CREATE SEQUENCE fayrpg.houses_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE fayrpg.houses_id_seq;
       fayrpg          postgres    false    219    5            7           0    0    houses_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE fayrpg.houses_id_seq OWNED BY fayrpg.houses.id;
          fayrpg          postgres    false    218            �            1259    16467    housetypes_id_seq    SEQUENCE     �   CREATE SEQUENCE fayrpg.housetypes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE fayrpg.housetypes_id_seq;
       fayrpg          postgres    false    5    225            8           0    0    housetypes_id_seq    SEQUENCE OWNED BY     H   ALTER SEQUENCE fayrpg.housetypes_id_seq OWNED BY fayrpg.house_types.id;
          fayrpg          postgres    false    224            �            1259    16511    inventory_items    TABLE     �   CREATE TABLE fayrpg.inventory_items (
    id integer NOT NULL,
    item_id integer,
    inventory_id integer,
    external_id integer,
    externaltype integer,
    description text,
    metadata integer
);
 #   DROP TABLE fayrpg.inventory_items;
       fayrpg         heap    postgres    false    5            �            1259    16510    invebtoryitem_id_seq    SEQUENCE     �   CREATE SEQUENCE fayrpg.invebtoryitem_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE fayrpg.invebtoryitem_id_seq;
       fayrpg          postgres    false    230    5            9           0    0    invebtoryitem_id_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE fayrpg.invebtoryitem_id_seq OWNED BY fayrpg.inventory_items.id;
          fayrpg          postgres    false    229            �            1259    16500 	   item_data    TABLE     {   CREATE TABLE fayrpg.item_data (
    item_id integer NOT NULL,
    weapon_id integer,
    type integer,
    heal integer
);
    DROP TABLE fayrpg.item_data;
       fayrpg         heap    postgres    false    5            �            1259    16492    items    TABLE     �   CREATE TABLE fayrpg.items (
    id integer NOT NULL,
    name text,
    max_amount integer,
    min_price integer,
    max_price integer,
    volume integer,
    sellable boolean,
    droppable boolean
);
    DROP TABLE fayrpg.items;
       fayrpg         heap    postgres    false    5            �            1259    16491    items_id_seq    SEQUENCE     �   CREATE SEQUENCE fayrpg.items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE fayrpg.items_id_seq;
       fayrpg          postgres    false    5    227            :           0    0    items_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE fayrpg.items_id_seq OWNED BY fayrpg.items.id;
          fayrpg          postgres    false    226            �            1259    16525    player_inventors    TABLE     �   CREATE TABLE fayrpg.player_inventors (
    id integer NOT NULL,
    player_id integer,
    item_id integer,
    amount integer,
    worn boolean,
    dead boolean,
    "where" integer
);
 $   DROP TABLE fayrpg.player_inventors;
       fayrpg         heap    postgres    false    5            �            1259    16524    playerinventors_id_seq    SEQUENCE     �   CREATE SEQUENCE fayrpg.playerinventors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE fayrpg.playerinventors_id_seq;
       fayrpg          postgres    false    5    232            ;           0    0    playerinventors_id_seq    SEQUENCE OWNED BY     R   ALTER SEQUENCE fayrpg.playerinventors_id_seq OWNED BY fayrpg.player_inventors.id;
          fayrpg          postgres    false    231            �            1259    16406    players    TABLE     1  CREATE TABLE fayrpg.players (
    id bigint NOT NULL,
    name text NOT NULL,
    password text NOT NULL,
    money integer DEFAULT 250000 NOT NULL,
    skin integer DEFAULT 26 NOT NULL,
    admin integer DEFAULT 0 NOT NULL,
    sex bit(1),
    playedtime bigint DEFAULT 0 NOT NULL,
    birthdate date
);
    DROP TABLE fayrpg.players;
       fayrpg         heap    postgres    false    5            �            1259    16405    players_id_seq    SEQUENCE     w   CREATE SEQUENCE fayrpg.players_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 %   DROP SEQUENCE fayrpg.players_id_seq;
       fayrpg          postgres    false    5    217            <           0    0    players_id_seq    SEQUENCE OWNED BY     A   ALTER SEQUENCE fayrpg.players_id_seq OWNED BY fayrpg.players.id;
          fayrpg          postgres    false    216            |           2604    16471    house_types id    DEFAULT     o   ALTER TABLE ONLY fayrpg.house_types ALTER COLUMN id SET DEFAULT nextval('fayrpg.housetypes_id_seq'::regclass);
 =   ALTER TABLE fayrpg.house_types ALTER COLUMN id DROP DEFAULT;
       fayrpg          postgres    false    224    225    225            {           2604    16433 	   houses id    DEFAULT     f   ALTER TABLE ONLY fayrpg.houses ALTER COLUMN id SET DEFAULT nextval('fayrpg.houses_id_seq'::regclass);
 8   ALTER TABLE fayrpg.houses ALTER COLUMN id DROP DEFAULT;
       fayrpg          postgres    false    218    219    219            ~           2604    16514    inventory_items id    DEFAULT     v   ALTER TABLE ONLY fayrpg.inventory_items ALTER COLUMN id SET DEFAULT nextval('fayrpg.invebtoryitem_id_seq'::regclass);
 A   ALTER TABLE fayrpg.inventory_items ALTER COLUMN id DROP DEFAULT;
       fayrpg          postgres    false    230    229    230            }           2604    16495    items id    DEFAULT     d   ALTER TABLE ONLY fayrpg.items ALTER COLUMN id SET DEFAULT nextval('fayrpg.items_id_seq'::regclass);
 7   ALTER TABLE fayrpg.items ALTER COLUMN id DROP DEFAULT;
       fayrpg          postgres    false    226    227    227                       2604    16528    player_inventors id    DEFAULT     y   ALTER TABLE ONLY fayrpg.player_inventors ALTER COLUMN id SET DEFAULT nextval('fayrpg.playerinventors_id_seq'::regclass);
 B   ALTER TABLE fayrpg.player_inventors ALTER COLUMN id DROP DEFAULT;
       fayrpg          postgres    false    232    231    232            v           2604    16409 
   players id    DEFAULT     h   ALTER TABLE ONLY fayrpg.players ALTER COLUMN id SET DEFAULT nextval('fayrpg.players_id_seq'::regclass);
 9   ALTER TABLE fayrpg.players ALTER COLUMN id DROP DEFAULT;
       fayrpg          postgres    false    216    217    217            (          0    16468    house_types 
   TABLE DATA           i   COPY fayrpg.house_types (id, enter_x, enter_y, enter_z, angle, interior, description, price) FROM stdin;
    fayrpg          postgres    false    225   A       &          0    16430    houses 
   TABLE DATA           �   COPY fayrpg.houses (id, entry_x, entry_y, entry_z, angle, owner_id, type, locked, interior, price, housetype_id, rentdate) FROM stdin;
    fayrpg          postgres    false    219   pE       -          0    16511    inventory_items 
   TABLE DATA           v   COPY fayrpg.inventory_items (id, item_id, inventory_id, external_id, externaltype, description, metadata) FROM stdin;
    fayrpg          postgres    false    230   �E       +          0    16500 	   item_data 
   TABLE DATA           C   COPY fayrpg.item_data (item_id, weapon_id, type, heal) FROM stdin;
    fayrpg          postgres    false    228   �E       *          0    16492    items 
   TABLE DATA           h   COPY fayrpg.items (id, name, max_amount, min_price, max_price, volume, sellable, droppable) FROM stdin;
    fayrpg          postgres    false    227   �E       /          0    16525    player_inventors 
   TABLE DATA           _   COPY fayrpg.player_inventors (id, player_id, item_id, amount, worn, dead, "where") FROM stdin;
    fayrpg          postgres    false    232   F       $          0    16406    players 
   TABLE DATA           e   COPY fayrpg.players (id, name, password, money, skin, admin, sex, playedtime, birthdate) FROM stdin;
    fayrpg          postgres    false    217   1F       =           0    0    houses_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('fayrpg.houses_id_seq', 1, true);
          fayrpg          postgres    false    218            >           0    0    housetypes_id_seq    SEQUENCE SET     A   SELECT pg_catalog.setval('fayrpg.housetypes_id_seq', 43, false);
          fayrpg          postgres    false    224            ?           0    0    invebtoryitem_id_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('fayrpg.invebtoryitem_id_seq', 1, false);
          fayrpg          postgres    false    229            @           0    0    items_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('fayrpg.items_id_seq', 1, false);
          fayrpg          postgres    false    226            A           0    0    playerinventors_id_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('fayrpg.playerinventors_id_seq', 1, false);
          fayrpg          postgres    false    231            B           0    0    players_id_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('fayrpg.players_id_seq', 1, true);
          fayrpg          postgres    false    216            �           2606    16435    houses houses_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY fayrpg.houses
    ADD CONSTRAINT houses_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY fayrpg.houses DROP CONSTRAINT houses_pkey;
       fayrpg            postgres    false    219            �           2606    16475    house_types housetypes_pkey 
   CONSTRAINT     Y   ALTER TABLE ONLY fayrpg.house_types
    ADD CONSTRAINT housetypes_pkey PRIMARY KEY (id);
 E   ALTER TABLE ONLY fayrpg.house_types DROP CONSTRAINT housetypes_pkey;
       fayrpg            postgres    false    225            �           2606    16518     inventory_items invebtoryitem_pk 
   CONSTRAINT     ^   ALTER TABLE ONLY fayrpg.inventory_items
    ADD CONSTRAINT invebtoryitem_pk PRIMARY KEY (id);
 J   ALTER TABLE ONLY fayrpg.inventory_items DROP CONSTRAINT invebtoryitem_pk;
       fayrpg            postgres    false    230            �           2606    16504    item_data item_data_pk 
   CONSTRAINT     Y   ALTER TABLE ONLY fayrpg.item_data
    ADD CONSTRAINT item_data_pk PRIMARY KEY (item_id);
 @   ALTER TABLE ONLY fayrpg.item_data DROP CONSTRAINT item_data_pk;
       fayrpg            postgres    false    228            �           2606    16499    items items_pk 
   CONSTRAINT     L   ALTER TABLE ONLY fayrpg.items
    ADD CONSTRAINT items_pk PRIMARY KEY (id);
 8   ALTER TABLE ONLY fayrpg.items DROP CONSTRAINT items_pk;
       fayrpg            postgres    false    227            �           2606    16530 #   player_inventors playerinventors_pk 
   CONSTRAINT     a   ALTER TABLE ONLY fayrpg.player_inventors
    ADD CONSTRAINT playerinventors_pk PRIMARY KEY (id);
 M   ALTER TABLE ONLY fayrpg.player_inventors DROP CONSTRAINT playerinventors_pk;
       fayrpg            postgres    false    232            �           2606    16413    players players_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY fayrpg.players
    ADD CONSTRAINT players_pkey PRIMARY KEY (id);
 >   ALTER TABLE ONLY fayrpg.players DROP CONSTRAINT players_pkey;
       fayrpg            postgres    false    217            �           2606    16476    houses FK_houses_houstype    FK CONSTRAINT     �   ALTER TABLE ONLY fayrpg.houses
    ADD CONSTRAINT "FK_houses_houstype" FOREIGN KEY (housetype_id) REFERENCES fayrpg.house_types(id) NOT VALID;
 E   ALTER TABLE ONLY fayrpg.houses DROP CONSTRAINT "FK_houses_houstype";
       fayrpg          postgres    false    219    4741    225            �           2606    16436    houses FK_houses_owner    FK CONSTRAINT     z   ALTER TABLE ONLY fayrpg.houses
    ADD CONSTRAINT "FK_houses_owner" FOREIGN KEY (owner_id) REFERENCES fayrpg.players(id);
 B   ALTER TABLE ONLY fayrpg.houses DROP CONSTRAINT "FK_houses_owner";
       fayrpg          postgres    false    4737    219    217            �           2606    16519 )   inventory_items invebtoryitem_items_id_fk    FK CONSTRAINT     �   ALTER TABLE ONLY fayrpg.inventory_items
    ADD CONSTRAINT invebtoryitem_items_id_fk FOREIGN KEY (item_id) REFERENCES fayrpg.items(id);
 S   ALTER TABLE ONLY fayrpg.inventory_items DROP CONSTRAINT invebtoryitem_items_id_fk;
       fayrpg          postgres    false    230    4743    227            �           2606    16505    item_data item_data_item_fk    FK CONSTRAINT     z   ALTER TABLE ONLY fayrpg.item_data
    ADD CONSTRAINT item_data_item_fk FOREIGN KEY (item_id) REFERENCES fayrpg.items(id);
 E   ALTER TABLE ONLY fayrpg.item_data DROP CONSTRAINT item_data_item_fk;
       fayrpg          postgres    false    227    4743    228            �           2606    16541 (   player_inventors playerinventors_item_fk    FK CONSTRAINT     �   ALTER TABLE ONLY fayrpg.player_inventors
    ADD CONSTRAINT playerinventors_item_fk FOREIGN KEY (item_id) REFERENCES fayrpg.inventory_items(id);
 R   ALTER TABLE ONLY fayrpg.player_inventors DROP CONSTRAINT playerinventors_item_fk;
       fayrpg          postgres    false    230    232    4747            �           2606    16531 *   player_inventors playerinventors_player_fk    FK CONSTRAINT     �   ALTER TABLE ONLY fayrpg.player_inventors
    ADD CONSTRAINT playerinventors_player_fk FOREIGN KEY (player_id) REFERENCES fayrpg.players(id);
 T   ALTER TABLE ONLY fayrpg.player_inventors DROP CONSTRAINT playerinventors_player_fk;
       fayrpg          postgres    false    217    4737    232            (   C  x�uVI�\7\��hA��;d�e6	��q9}��=���/��*�U�x��!�FUM������,����o����!8��O�'�%Ӥ�	�����������*�*ܲU����T*{��_�<�>������OZ�в5]8��l��
T�sF����EB� ��)R�Ꭵu�a�eB�D�i��JF�ˇ��)�n��	�qC�ƆZ�Y���
D�X�o(r͇�8�ȁ�f�� `&���W���W�D�ư3Q��F��e1�$P�5������_Q�;�e9�6G��[<x����|�-W���u�:Ӆ�8����ԇ5�@�@�R�+���:je(�ֶ�+l��@�h�t�y[X�=�[лs���{B��.T����Rf&?Aﾇo��j�<�ͣ3�W���^Q�v��B�7�p���35ȚaK��o�ǎ�`c&��4�&�?�L��j��_��q�b��R�#sN��Q��.y �����4�V��mj)����BW����o��:�!HC��*���l���-M�ġ]���B�[z�&ͳ��D�k�ə�ŗ���F���&�yO^�L�Kk.�P��x2h�w���f�@�'|�jz�q`�P�B�ߢ�{�A��{�:�7��e��	H�����T�I�aË��F �Pt��f*�z�aхEl]��.%�v���z��_��g5o'C� �8���7��7��PP��D7P	k���@Qu��B�m���sp��9T!�^s��'@�X��\ǆ� ��?f��Id��@�I�X@�Wv�	lc��=E�w������AD��CLM?t���� ��J�7.�m u��a$�{_ٕ�:��]�
�.+��pVb�-Ӽ��aO��1�g#B���`g����] ��1�����-q��CZ��mZ@���wE�)#�hM`�k%�8~����/߾>��b�F�f�{�Ad�gD��������B7���ђmj�f<�x9DO[+�>����{��t
�Q�+Z����y��Ӕop��:<;Д���8`��Y����C�U;��͏��}��      &   =   x����0����MI�.}w����&���։5���~z#��ՙ���)O�f�q
�      -      x������ � �      +      x������ � �      *      x������ � �      /      x������ � �      $   �   x��;! �?ۗH�v�XJ��9}h��ay������f;�	m1��Y�.�<�bGt`h::��5I2�a�6Y���sƈ��y��D]����c�A�fGi�QI 
*(�����H�������+�     