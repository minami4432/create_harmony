#n度上のハモリを生成するプログラム
import mido
import random
from mido import Message, MidiFile, MidiTrack

#毎回変える部分
hamo = 3 #ハモリの度数. 1~6の整数．
key = 4 #キー．0~11の整数．Cが0.
mid_original = '3_5_melody'

mid_original_name = f'{mid_original}.mid'
new_mid_name = f'{mid_original}_{hamo}_hamo.mid'

melody = [] #入力したメロディ
adapt = [0, 0, 1, 0, 2, 3, 0, 4, 0, 5, 0, 6] #12音階を0~6の数字に変換
scale = [2, 2, 1, 2, 2, 2, 1] #メジャースケール
degree = [] #度数
new_melody = []
length_of_note = []
vel=90

def create_harmony(mid_original_name, new_mid_name, hamo):
    mid = MidiFile(mid_original_name)
    new_mid = MidiFile() #新しいMIDIファイルを作成
    track = mid.tracks[0]
    new_track = MidiTrack()
    new_mid.tracks.append(new_track)
    
    #midの音程をmelodyに格納
    for i in enumerate(mid.tracks):
        for msg in track:
            if msg.type == 'note_on':
                melody.append(msg.note)
                degree.append(0)
                new_melody.append(0)
            elif msg.type == 'note_off':
                length_of_note.append(msg.time)
        print(melody)
        print(length_of_note)
    for i in range(len(melody)):
            new_melody[i] = melody[i]
            #元の音程の度数を取得
            degree[i] = adapt[(melody[i] + 12 - key) % 12]
            for j in range(hamo):
                new_melody[i] += scale[(degree[i])] #1か2
                degree[i] = adapt[(new_melody[i] + 12 - key) % 12]
            # 新しい音符のメッセージを作成
            new_track.append(Message('note_on', note=new_melody[i], velocity=vel, time=0))
            new_track.append(Message('note_off', note=new_melody[i], velocity=vel, time=length_of_note[i]))
    new_mid.save(new_mid_name)

create_harmony(mid_original_name, new_mid_name, hamo)

